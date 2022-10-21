# scipy = 1.9.2, keras-ocr = 0.9.1, numpy = 1.23.4, pandas = 1.2.4, tensorflow = 2.10.0
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import difflib

import easyocr
import keras_ocr


class LabelPredictor:
    def __init__(self, relevant_labels):
        self.relevant_labels = None
        self.reader = easyocr.Reader(['en'], gpu=True)
        self.process_relevant_labels(relevant_labels)

    # Obtains usable df format for the given relevant labels (.csv)
    def process_relevant_labels(self, relevant_labels):
        temp_relevant_labels = pd.read_csv(relevant_labels)
        temp_relevant_labels['Labels'] = temp_relevant_labels['Labels'].apply(
            lambda x: list(map(lambda y: y.upper(), x.split(';'))))
        self.relevant_labels = temp_relevant_labels

    def predict_labels(self, img):
        # Predicts text labels on given image
        result = self.reader.readtext(img)
        dfs = []
        camera_id = int(img.split('/')[-1].split('.')[0].split('_')[0])
        true_labels = self.relevant_labels[self.relevant_labels.Camera_Id ==
                                           camera_id].Labels
        true_labels = [item for sublist in true_labels for item in sublist]

        filtered_results = []
        for labels in result:
            label = labels[1].upper()
            if label not in true_labels:
                matched_labels = difflib.get_close_matches(label, true_labels)
            else:
                matched_labels = [label]
            if len(matched_labels) == 0:
                continue
            matched_label = matched_labels[0]
            temp_label = list(labels)
            temp_label[1] = matched_label
            labels = tuple(temp_label)
            filtered_results.append(labels)
        img_id = img.split(".")[1].split("/")[-1]
        img_df = pd.DataFrame(filtered_results, columns=[
                              'bbox', 'text', 'conf'])
        img_df['img_id'] = img_id
        dfs.append(img_df)
        easyocr_df = pd.concat(dfs)
        fig, axs = plt.subplots(figsize=(10, 10))

        easy_results = easyocr_df.query(
            'img_id == @img_id')[['text', 'bbox']].values.tolist()
        easy_results = [(x[0], np.array(x[1])) for x in easy_results]
        keras_ocr.tools.drawAnnotations(plt.imread(img),
                                        easy_results, ax=axs)
        axs.set_title(camera_id, fontsize=24)
        plt.show()


### TESTS ###

predictor = LabelPredictor('label_filters.csv')
predictor.predict_labels(
    './sharepoint/2022_01_05_22_00/1707_2154_20220105215512_d74cd3.jpg')

############
