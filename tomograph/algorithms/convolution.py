class Convolution:
    def transform(self, image, mask=None):
        result = []
        if mask is None:
            mask = [-1, 3, 1]
        for i in range(0, len(image)):
            result.append([])
            for j in range(1, (len(image[i]) - 1)):
                result[i].append(mask[0] * image[i][j - 1] + mask[1] * image[i][j] + mask[2] * image[i][j + 1])
        return result
