from matcher import ImageMatcher


class ChatbotEngine:
    def __init__(self):
        pass

    def process_image(self, image):
        image_matcher = ImageMatcher(image)
        np_arr = image_matcher._load_image()
        print(np_arr)
