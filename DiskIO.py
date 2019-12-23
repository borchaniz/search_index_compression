import pickle


class DiskIO:
    def __compress_1_number_vbe(self, number):
        binary = bin(number)[2:]
        res = ''
        i = 0
        while len(binary) > 7:
            res = '0' + binary[len(binary) - 7:] + res
            binary = binary[:len(binary) - 7]
            i += 1
        res = '1' + binary.zfill(7) + res
        i += 1
        return int(res, base=2), i

    def __compress_vbe(self, numbers):
        res = 0
        for number in numbers:
            compressed = self.__compress_1_number_vbe(number)
            res = (res << (compressed[1] * 8)) + compressed[0]
        return res

    def __decompress_vbe(self, compressed_int):
        res = []
        compressed_str = bin(compressed_int)[2:]
        while len(compressed_str) > 0:
            temp = ''
            while len(compressed_str) > 0 and compressed_str[len(compressed_str) - 8] == '0':
                temp = compressed_str[len(compressed_str) - 7:] + temp
                compressed_str = compressed_str[:len(compressed_str) - 8]
            temp = compressed_str[len(compressed_str) - 7:] + temp
            compressed_str = compressed_str[:len(compressed_str) - 8]
            res = [int(temp, base=2)] + res
        return res

    def __compress_gap(self, numbers):
        res = [numbers[0]]
        for index in range(1, len(numbers)):
            res.append(numbers[index] - numbers[index - 1])
        return res

    def __decompress_gap(self, compressed):
        res = [compressed[0]]
        for index in range(1, len(compressed)):
            res.append(compressed[index] + res[index - 1])
        return res

    def __string_to_nbr(self, doc_id):
        result = 0
        for char in doc_id:
            result = result << 8
            result += ord(char)
        return result

    def __nbr_to_string(self, nbr):
        result = ''
        while nbr > 0:
            temp = nbr % 256
            nbr = nbr >> 8
            result = chr(temp) + result
        return result

    def __compress(self, dictionary):
        result = []
        last_key = 0
        int_keys = []
        for key in dictionary.keys():
            int_keys.append(self.__string_to_nbr(key))
        for key in sorted(int_keys):
            result.append(key - last_key)
            last_key = key
            key = self.__nbr_to_string(key)
            result.append(len(dictionary[key]))
            result = result + self.__compress_gap(dictionary[key])
        return self.__compress_vbe(result)

    def decompress(self, vbe_compressed):
        result = {}
        compressed_list = self.__decompress_vbe(vbe_compressed)
        int_key = 0
        while len(compressed_list) > 0:
            temp = compressed_list.pop(0)
            int_key = int_key + temp
            key = self.__nbr_to_string(int_key)
            length = compressed_list.pop(0)
            result[key] = self.__decompress_gap(compressed_list[:length])
            compressed_list = compressed_list[length:]
        return result

    def __compress_all(self, dictionary):
        res = {}
        for key in dictionary:
            res[key] = self.__compress(dictionary[key])
        return res

    def __decompress_all(self, compressed):
        res = {}
        for key in compressed:
            res[key] = self.decompress(compressed[key])
        return res

    def write(self, index, file_name):
        with open(file_name, 'wb') as outfile:
            pickle.dump(self.__compress_all(index), outfile)

    def read_and_decompress(self, file_name):
        with open(file_name, 'rb') as infile:
            saved = pickle.load(infile)
        return self.__decompress_all(saved)

    def read(self, file_name):
        with open(file_name, 'rb') as infile:
            saved = pickle.load(infile)
        return saved
