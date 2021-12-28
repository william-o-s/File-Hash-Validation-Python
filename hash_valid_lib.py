import hashlib

def get_avail_hash_types() -> list:
    """Returns a set of all the available hash types for calculation.
    """
    return HashFile("").hash_objects.keys()

class HashFile:
    def __init__(self, target_file_addr: str) -> None:
        """Helper class for calculating file hashes. A new HashFile object
        should be created for every hash process.

        @target_file_addr: The target file's directory address.
        """
        self.file_addr = target_file_addr
        self.hash_objects = self.new_hash_objects()
    
    def new_hash_objects(self) -> dict:
        """Returns a new set of hashlib hash-type objects.
        
        NOTE: The purpose of this method is due to the functionality of hashlib.
        Whenever a hash-type object is instantiated, e.g. through md5() or
        sha1(), and update() is called on it, a chunk of data is hashed and
        added to a cache to avoid recalculating previous chunks. This is memory
        efficient but has the consequence of adding new data to previous data
        when update() is called again, i.e. if the object is called on a second
        file, its hash is calculating by adding the data of the first file.
        Thus, new hash-type objects must be generated for new files.
        """
        return {
            "MD5": hashlib.md5(),
            "SHA1": hashlib.sha1(),
            "SHA256": hashlib.sha256()
        }
    
    def hashCalculate(self, hash_type: str) -> str:
        """Returns the calculation of a specified hash type of a file.
        
        @hash_type: The hash type to be calculated (as a string)

        ### Possible errors:
            - Incorrect/Invalid directory address: throws a FileNotFoundError
            - Corrupt file data: throws 
        """
        try:
            # Read and update hash string value in 4k chunks to avoid large
            # memory usage errors
            with open(self.file_addr, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    self.hash_objects[hash_type].update(byte_block)
            return self.hash_objects[hash_type].hexdigest()

        except FileNotFoundError:
            print("FileNotFoundError occurred. Is the address valid?")
            return None

        except:
            print("Unknown Exception occurred. Is the file corrupt?")
            return None
