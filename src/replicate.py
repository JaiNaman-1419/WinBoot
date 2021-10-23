import stat
from sys import audit
from os.path import join, exists, isdir, isfile, getsize
from shutil import copy, copy2, copystat, Error, COPY_BUFSIZE
from os import fspath, makedirs, name, readlink, symlink, scandir, listdir


class Replica:

    def __init__(self):
        self.__READINTO_BUFFER = 1024 * 1024

    def get_read_to_buffer(self):
        return self.__READINTO_BUFFER

    def _copytree(self, entries, src, dst, flash_screen, callback, symlinks, ignore, copy_function,
                  ignore_dangling_symlinks, dirs_exist_ok=False):
        if ignore is not None:
            ignored_names = ignore(fspath(src), [x.name for x in entries])
        else:
            ignored_names = set()

        makedirs(dst, exist_ok=dirs_exist_ok)
        errors = []
        use_srcentry = copy_function is copy2 or copy_function is copy

        for srcentry in entries:
            if srcentry.name in ignored_names:
                continue
            src_name = join(src, srcentry.name)
            dst_name = join(dst, srcentry.name)
            src_obj = srcentry if use_srcentry else src_name
            try:
                is_symlink = srcentry.is_symlink()
                if is_symlink and name == 'nt':
                    # Special check for directory junctions, which appear as
                    # symlinks but we want to recurse.
                    lstat = srcentry.stat(follow_symlinks=False)
                    if lstat.st_reparse_tag == stat.IO_REPARSE_TAG_MOUNT_POINT:
                        is_symlink = False
                if is_symlink:
                    link_to = readlink(src_name)
                    if symlinks:
                        # We can't just leave it to `copy_function` because legacy
                        # code with a custom `copy_function` may rely on copytree
                        # doing the right thing.
                        symlink(link_to, dst_name)
                        copystat(src_obj, dst_name, follow_symlinks=not symlinks)
                    else:
                        # ignore dangling symlink if the flag is on
                        if not exists(link_to) and ignore_dangling_symlinks:
                            continue
                        # otherwise let the copy occur. copy2 will raise an error
                        if srcentry.is_dir():
                            self.copytree(src_obj, dst_name, flash_screen, callback, symlinks, ignore,
                                          copy_function, dirs_exist_ok=dirs_exist_ok)
                        else:
                            copy_function(src_obj, dst_name)
                        # Manual entry
                        callback(flash_screen)

                elif srcentry.is_dir():
                    self.copytree(src_obj, dst_name, flash_screen, callback, symlinks, ignore, copy_function,
                                  dirs_exist_ok=dirs_exist_ok)
                else:
                    # Will raise a SpecialFileError for unsupported file types
                    copy_function(src_obj, dst_name)

                    # Manual entry
                    callback(flash_screen)

            # catch the Error from the recursive copytree so that we can
            # continue with other files
            except Error as err:
                errors.extend(err.args[0])
            except OSError as why:
                errors.append((src_name, dst_name, str(why)))
        try:
            copystat(src, dst)
        except OSError as why:
            # Copying file access times may fail on Windows
            if getattr(why, 'winerror', None) is None:
                errors.append((src, dst, str(why)))
        if errors:
            raise Error(errors)
        return dst

    def copytree(self, src, dst, flash_screen, callback, symlinks=False, ignore=None, copy_function=copy2,
                 ignore_dangling_symlinks=False, dirs_exist_ok=False):
        audit("shutil.copytree", src, dst)
        with scandir(src) as itr:
            entries = list(itr)
        return self._copytree(entries=entries, src=src, dst=dst, flash_screen=flash_screen, callback=callback, symlinks=symlinks,
                              ignore=ignore, copy_function=copy_function,
                              ignore_dangling_symlinks=ignore_dangling_symlinks,
                              dirs_exist_ok=dirs_exist_ok)

    def copyfileobj(self, fsrc, fdst, flash_screen, callback, length=0):
        try:
            # check for optimisation opportunity
            if "b" in fsrc.mode and "b" in fdst.mode and fsrc.readinto:
                return self._copyfileobj_readinto(fsrc, fdst, flash_screen, callback, length)
        except AttributeError:
            # one or both file objects do not support a .   mode or .readinto attribute
            pass

        if not length:
            length = COPY_BUFSIZE

        fsrc_read = fsrc.read
        fdst_write = fdst.write

        # copied = 0
        while True:
            buf = fsrc_read(length)
            if not buf:
                break
            fdst_write(buf)
            # copied += len(buf)
            callback(flash_screen)

    def _copyfileobj_readinto(self, fsrc, fdst, flash_screen, callback, length=0):
        fsrc_readinto = fsrc.readinto
        fdst_write = fdst.write

        if not length:
            try:
                file_size = stat(fsrc.fileno()).st_size
            except OSError:
                file_size = self.get_read_to_buffer()
            length = min(file_size, self.get_read_to_buffer())

        # copied = 0
        with memoryview(bytearray(length)) as mv:
            while True:
                n = fsrc_readinto(mv)
                if not n:
                    break
                elif n < length:
                    with mv[:n] as smv:
                        fdst.write(smv)
                else:
                    fdst_write(mv)
                # copied += n
                callback(flash_screen)

    def get_folder_size(self, folder):
        total_size = getsize(folder)
        for item in listdir(folder):
            item_path = join(folder, item)
            if isfile(item_path):
                total_size += getsize(item_path)
            elif isdir(item_path):
                total_size += self.get_folder_size(item_path)
        return total_size
