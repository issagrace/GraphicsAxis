import cv2
import numpy as np

class DCT_Watermark:
    
    @staticmethod
    def __gene_signature(wm, size):
        wm = cv2.resize(wm, (size, size))
        wm = np.where(wm < np.mean(wm),0 , 1)
        return wm

    def embed(self, cover, wm):
        sig_size =200
        B = None
        img = None
        signature = None    
        if len(cover.shape) > 2:
            img = cv2.cvtColor(cover, cv2.COLOR_BGR2YUV)
            signature = self.__gene_signature(wm, sig_size).flatten()
            B = img[:, :, 0]

        if len(cover.shape) > 2:
            img[:, :, 0] = self.inner_embed(B, signature)
            cover = cv2.cvtColor(img, cv2.COLOR_YUV2BGR)
        else:
            cover = B
        return cover
    Q =  20
    size = 2
    sig_size =200

    def inner_embed(self, B: np.ndarray, signature):
        sig_size = self.sig_size
        size = self.size

        w, h = B.shape[:2]
        embed_pos = [(0, 0)]
        if w > 2 * sig_size * size:
            embed_pos.append((w-sig_size*size, 0))
        if h > 2 * sig_size * size:
            embed_pos.append((0, h-sig_size*size))
        if len(embed_pos) == 4:
            embed_pos.append((w-sig_size*size, h-sig_size*size))

        for x, y in embed_pos:
            for i in range(x, x+sig_size * size, size):
                for j in range(y, y+sig_size*size, size):
                    v = np.float32(B[i:i + size, j:j + size])
                    v = cv2.dct(v)
                    v[size-1, size-1] = self.Q * \
                        signature[((i-x)//size) * sig_size + (j-y)//size]
                    v = cv2.idct(v)
                    maximum = max(v.flatten())
                    minimum = min(v.flatten())
                    if maximum > 255:
                        v = v - (maximum - 255)
                    if minimum < 0:
                        v = v - minimum
                    B[i:i+size, j:j+size] = v
        return B