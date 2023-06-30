import shap
import pandas as pd
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix
from sklearn.model_selection import train_test_split
from dash import html

from sklearn.preprocessing import LabelEncoder
from explainers.explainers_plots import plotly_confusion_matrix, plotly_roc_curve


class BaseExplainer:

    def __init__(self, model, dataset=None):
        self.dataset = dataset
        self.labels = dataset.columns
        self.model = model
        self.X = dataset.iloc[:, :-1].values
        self.target = dataset.iloc[:, -1].values
        self.targets = pd.unique(self.target)
        label_encoder = LabelEncoder()
        self.Y = label_encoder.fit_transform(self.target)
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X, self.Y, test_size=.3)

    # stratify = dataset['Survival']
    def shap(self):
        explainer = shap.KernelExplainer(self.model.predict_proba, self.X_train)
        shap_values = explainer.shap_values(self.X_test)
        force_plot = shap.force_plot(explainer.expected_value[0], shap_values[0], self.X_test)
        shap_html = f"<head>{shap.getjs()}</head><body>{force_plot.html()}</body>"
        return html.Iframe(srcDoc=shap_html, style={"width": "100%", "height": "500px", "margin": "20px",
                                                    "border": 0})


class ClassifierExplainer(BaseExplainer):

    def __init__(self, model, datasets):
        super().__init__(model, datasets)

    def roc_auc_curve(self):
        y_scores = self.model.predict_proba(self.X)
        y_onehot = pd.get_dummies(self.target, columns=self.model.classes_)
        data = []
        for i in range(y_scores.shape[1]):
            y_true = y_onehot.iloc[:, i]
            y_score = y_scores[:, i]

            fpr, tpr, _ = roc_curve(y_true, y_score)
            auc_score = roc_auc_score(y_true, y_score)

            temp = [f"{y_onehot.columns[i]} (AUC={auc_score:.2f})", fpr, tpr]
            data.append(temp)

        return plotly_roc_curve(data)

    def confusion_matrix(self, binary=True, pos_label=None):
        # Make predictions on the test set
        y_pred = self.model.predict(self.X_test)

        # Calculate the confusion matrix and plot it using plotly.
        cm = confusion_matrix(self.Y_test, y_pred)

        # Change value to text for annotations.
        z_text = [[str(y) for y in x] for x in cm]

        return plotly_confusion_matrix(cm, self.targets, z_text)


class RegressionExplainer(BaseExplainer):

    def __init__(self, model, datasets):
        super().__init__(model, datasets)

    def predicted_vs_actual(self):
        pass

    def residual(self):
        pass
