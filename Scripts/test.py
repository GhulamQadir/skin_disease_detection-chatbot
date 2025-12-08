from dataset_preprocessor import DatasetPreprocessor


def test():
    root_path = "dataset"
    folders = ["Melanoma", "Chickenpox", "Herpes", "Eczema", "Acne", "Lupus"]
    preprocess = DatasetPreprocessor(root_path, folders)
    preprocess.prepare_dataset(50)


if __name__ == "__main__":
    test()
