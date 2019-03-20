class Convolution:
    def transform(self, image, mask=None):
        result = []
        if mask is None:
            mask = [-3, 7, -3]
        for i in range(0, len(image)):
            result.append([])
            result[i].append(image[i][0])
            for j in range(1, (len(image[i]) - 1)):
                value = mask[0] * image[i][j - 1] + mask[1] * image[i][j] + mask[2] * image[i][j + 1]
                if value > 255:
                    value = 255
                elif value < 0:
                    value = 0
                result[i].append(value)
            result[i].append(image[i][len(image[i]) - 1])
        return result
