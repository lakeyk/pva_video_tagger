"""Upload the contents of your Downloads folder to Dropbox.

This is an example app for API v2.
"""

from __future__ import print_function

import argparse
import contextlib
import datetime
import os
import six
import sys
import time
import unicodedata
from tqdm import tqdm
import dropbox


class DropboxSync:

    # OAuth2 access token.  TODO: login etc.

    def __init__(self):
        self.token = 'aZH12G9Qp50AAAAAAAAAAcjBcaEXbH3lOQJN_bdGtvfmH3AR7jYxhqrAbp9dsrmc'
        self.default = True
        self.yes = True
        self.no = False

    def sync(self, folder, rootdir):
        """Main program.

        Parse command line, then iterate over files and directories under
        rootdir and upload all files.  Skips some temporary files and
        directories, and avoids duplicate uploads by comparing size and
        mtime with the server.
        """
        if not self.token:
            print('--token is mandatory')
            sys.exit(2)
    
        print('Dropbox folder name:', folder)
        print('Local directory:', rootdir)
        if not os.path.exists(rootdir):
            print(rootdir, 'does not exist on your filesystem')
            sys.exit(1)
        elif not os.path.isdir(rootdir):
            print(rootdir, 'is not a folder on your filesystem')
            sys.exit(1)

        dbx = dropbox.Dropbox(self.token)

        for dn, dirs, files in os.walk(rootdir):
            subfolder = dn[len(rootdir):].strip(os.path.sep)
            listing = self.list_folder(dbx, folder, subfolder)
            print('Descending into', subfolder, '...')

            # First do all the files.
            for name in files:
                fullname = os.path.join(dn, name)
                if not isinstance(name, six.text_type):
                    name = name.decode('utf-8')
                nname = unicodedata.normalize('NFC', name)
                if name.startswith('.'):
                    print('Skipping dot file:', name)
                elif name.startswith('@') or name.endswith('~'):
                    print('Skipping temporary file:', name)
                elif name.endswith('.pyc') or name.endswith('.pyo'):
                    print('Skipping generated file:', name)
                elif nname in listing:
                    md = listing[nname]
                    mtime = os.path.getmtime(fullname)
                    mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
                    size = os.path.getsize(fullname)
                    if (isinstance(md, dropbox.files.FileMetadata) and
                            mtime_dt == md.client_modified and size == md.size):
                        print(name, 'is already synced [stats match]')
                    else:
                        print(name, 'already exists, refresh not enabled')
                elif self.yesno('Upload %s' % name, True):
                    self.upload(dbx, fullname, folder, subfolder, name)

            # Then choose which subdirectories to traverse.
            keep = []
            for name in dirs:
                if name.startswith('.'):
                    print('Skipping dot directory:', name)
                elif name.startswith('@') or name.endswith('~'):
                    print('Skipping temporary directory:', name)
                elif name == '__pycache__':
                    print('Skipping generated directory:', name)
                elif self.yesno('Descend into %s' % name, True):
                    print('Keeping directory:', name)
                    keep.append(name)
                else:
                    print('OK, skipping directory:', name)
            dirs[:] = keep

        dbx.close()

    def list_folder(self, dbx, folder, subfolder):
        """List a folder.

        Return a dict mapping unicode filenames to
        FileMetadata|FolderMetadata entries.
        """
        path = '/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'))
        while '//' in path:
            path = path.replace('//', '/')
        path = path.rstrip('/')
        try:
            with self.stopwatch('list_folder'):
                res = dbx.files_list_folder(path)
        except dropbox.exceptions.ApiError as err:
            print('Folder listing failed for', path, '-- assumed empty:', err)
            return {}
        else:
            rv = {}
            for entry in res.entries:
                rv[entry.name] = entry
            return rv

    def download(self, dbx, folder, subfolder, name):
        """Download a file.
    
        Return the bytes of the file, or None if it doesn't exist.
        """
        path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
        while '//' in path:
            path = path.replace('//', '/')
        with self.stopwatch('download'):
            try:
                md, res = dbx.files_download(path)
            except dropbox.exceptions.HttpError as err:
                print('*** HTTP error', err)
                return None
        data = res.content
        print(len(data), 'bytes; md:', md)
        return data

    def upload(self, dbx, fullname, folder, subfolder, name, overwrite=False):
        """Upload a file.

        Return the request response, or None in case of error.
        """
        path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
        while '//' in path:
            path = path.replace('//', '/')
        mode = (dropbox.files.WriteMode.overwrite
                if overwrite
                else dropbox.files.WriteMode.add)
        mtime = os.path.getmtime(fullname)
        chunk_size = 4 * 1024 * 1024
        file_size = os.path.getsize(fullname)
        if file_size < chunk_size:
            return self.upload_small(dbx, fullname, mtime, path, mode)
        else:
            return self.upload_large(dbx, fullname, file_size, chunk_size, mtime, path, mode)

    def upload_small(self, dbx, fullname, mtime, path, mode):
        with open(fullname, 'rb') as f:
            with self.stopwatch('upload file size: ' + str(os.path.getsize(fullname))):
                try:
                    res = dbx.files_upload(f.read(), path, mode, client_modified=datetime.datetime(*time.gmtime(mtime)[:6]), mute=True)
                except dropbox.exceptions.ApiError as err:
                    print('*** API error', err)
                    return None
            print('uploaded as', res.name.encode('utf8'))
        return res
    

    def upload_large(self, dbx, fullname, file_size, chunk_size, mtime, target_path, mode):
        with open(fullname, 'rb') as f:
            with tqdm(total=file_size, desc="Uploaded") as pbar:
                upload_session_start_result = dbx.files_upload_session_start(f.read(chunk_size))
                pbar.update(chunk_size)
                cursor = dropbox.files.UploadSessionCursor(
                    session_id=upload_session_start_result.session_id,
                    offset=f.tell(),
                )
                commit = dropbox.files.CommitInfo(path=target_path)
                while f.tell() < file_size:
                    if (file_size - f.tell()) <= chunk_size:
                        print(
                            dbx.files_upload_session_finish(
                                f.read(chunk_size), cursor, commit
                            )
                        )
                    else:
                        dbx.files_upload_session_append(
                            f.read(chunk_size),
                            cursor.session_id,
                            cursor.offset,
                        )
                        cursor.offset = f.tell()
                    pbar.update(chunk_size)
    
    def yesno(self, message, default):
        """Handy helper function to ask a yes/no question.

        Command line arguments --yes or --no force the answer;
        --default to force the default answer.

        Otherwise a blank line returns the default, and answering
        y/yes or n/no returns True or False.

        Retry on unrecognized answer.
    
        Special answers:
        - q or quit exits the program
        - p or pdb invokes the debugger
        """
        if self.default:
            print(message + '? [auto]', 'Y' if default else 'N')
            return default
        if self.yes:
            print(message + '? [auto] YES')
            return True
        if self.no:
            print(message + '? [auto] NO')
            return False
        if default:
            message += '? [Y/n] '
        else:
            message += '? [N/y] '
        while True:
            answer = input(message).strip().lower()
            if not answer:
                return default
            if answer in ('y', 'yes'):
                return True
            if answer in ('n', 'no'):
                return False
            if answer in ('q', 'quit'):
                print('Exit')
                raise SystemExit(0)
            if answer in ('p', 'pdb'):
                import pdb
                pdb.set_trace()
            print('Please answer YES or NO.')

    @contextlib.contextmanager
    def stopwatch(self, message):
        """Context manager to print how long a block of code took."""
        t0 = time.time()
        try:
            yield
        finally:
            t1 = time.time()
            print('Total elapsed time for %s: %.3f' % (message, t1 - t0))
