result1 = verify_download({"filename": "lesson01.mp4", "size": 15420, "checksum_valid": True})
result2 = verify_download({"filename": "lesson02.txt", "size": 8300, "checksum_valid": True})
result3 = verify_download({"filename": "lesson03.mp4", "size": 0, "checksum_valid": True})
result4 = verify_download({"filename": "lesson04.mp4", "size": 12000, "checksum_valid": False})
