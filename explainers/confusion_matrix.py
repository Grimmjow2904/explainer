import plotly.graph_objs as go
from dash import dcc
from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split

# Load the MNIST dataset
digits = datasets.load_digits()

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(digits.data, digits.target, test_size=0.2, random_state=42)

# Train the SVM model
clf = svm.SVC(gamma=0.001, C=100.)

# Fit the model to the training data
clf.fit(X_train, y_train)

# Make predictions on the testing data
y_pred = clf.predict(X_test)

# Generate the confusion matrix
cm = metrics.confusion_matrix(y_test, y_pred)

# Define the layout for the heatmap
layout = go.Layout(
    title="Confusion Matrix",
    xaxis=dict(title="Predicted Label"),
    yaxis=dict(title="True Label")
)

# Create the heatmap trace
trace = go.Heatmap(z=cm, x=list(range(10)), y=list(range(10)), colorscale="Viridis")

# Create the figure and plot it
fig = go.Figure(data=[trace], layout=layout)

graph = dcc.Graph(figure=fig)
