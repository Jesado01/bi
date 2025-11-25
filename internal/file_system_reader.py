import os
from pathlib import Path


class FileSystemReader:
    """File system reader with encoding handling and Windows long path support"""

    def __init__(self, base_path: str = None):
        if base_path:
            self.base_path = Path(base_path).resolve()
        else:
            self.base_path = None

    def read_file(self, file_path: str) -> str:
        file_p = Path(file_path)
        """Read file content with proper encoding detection and long path handling"""
        if self.base_path:
            full_path = (self.base_path / file_p).resolve()
        else:
            full_path = file_p.resolve()

        # Try standard approach first
        if full_path.exists():
            return self._read_with_encoding_fallback(full_path)

        # If standard approach fails, try alternative methods (handles Windows long paths)
        return self._try_alternative_reads(full_path)

    def _read_with_encoding_fallback(self, file_path: Path) -> str:
        """Read file with UTF-8 and Latin-1 fallback"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                print(f"Failed to read {file_path}: {str(e)}")
                return ""
        except Exception as e:
            print(f"Error reading {file_path}: {str(e)}")
            return ""

    def _try_alternative_reads(self, full_path: Path) -> str:
        """Try alternative methods for files that should exist but aren't accessible"""
        raw_path = str(full_path)

        # Method 1: UNC long path prefix for Windows paths > 260 characters
        if len(raw_path) > 260 and os.name == 'nt':
            try:
                unc_path = "\\\\?\\" + raw_path
                with open(unc_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except UnicodeDecodeError:
                try:
                    with open(unc_path, 'r', encoding='latin-1') as f:
                        return f.read()
                except:
                    pass
            except:
                pass

        # Method 2: Change to parent directory and use relative path
        try:
            original_dir = os.getcwd()
            parent_dir = full_path.parent
            filename = full_path.name

            os.chdir(str(parent_dir))
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                return content

        except UnicodeDecodeError:
            try:
                with open(filename, 'r', encoding='latin-1') as f:
                    return f.read()
            except:
                pass
        except Exception:
            pass
        finally:
            try:
                os.chdir(original_dir)
            except:
                pass

        # Method 3: Try pathlib is_file() which sometimes works when exists() doesn't
        try:
            p = Path(raw_path)
            if p.is_file():
                return self._read_with_encoding_fallback(p)
        except:
            pass

        # Method 4: Try shorter base path approach
        if self.base_path:
            try:
                shorter_base = self.base_path.parent.parent
                relative_from_shorter = full_path.relative_to(shorter_base)

                original_dir = os.getcwd()
                os.chdir(str(shorter_base))

                with open(str(relative_from_shorter), 'r', encoding='utf-8') as f:
                    content = f.read()
                    return content

            except UnicodeDecodeError:
                try:
                    with open(str(relative_from_shorter), 'r', encoding='latin-1') as f:
                        return f.read()
                except:
                    pass
            except Exception:
                pass
            finally:
                try:
                    os.chdir(original_dir)
                except:
                    pass

        # If all methods fail
        print(f"File not found or inaccessible: {full_path}")
        return ""

    def list_directory_contents(self, directory_path: str = None) -> list:
        """List contents of a directory"""
        if directory_path:
            if self.base_path:
                dir_path = self.base_path / directory_path
            else:
                dir_path = Path(directory_path)
        else:
            dir_path = self.base_path or Path.cwd()

        try:
            return [item.name for item in dir_path.iterdir()]
        except Exception as e:
            print(f"Error listing directory {dir_path}: {e}")
            return []
