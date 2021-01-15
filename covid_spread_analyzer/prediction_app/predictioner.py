from matplotlib import pyplot
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense, Dropout


def reshaper(x):
    return x.reshape((len(x), 1))


class Predictioner:
    def __init__(self):
        self.model = Sequential()
        self.setup_model()
        self.compile_model()

    def save_model(self, path):
        self.model.save(path)

    def load_model(self, path):
        self.model = keras.models.load_model(path)

    def update_input(self, train_x, train_y):
        self.push_train_sets(train_x, train_y)
        self.y_scaler = MinMaxScaler()
        self.x_scaler = MinMaxScaler()
        self.reshape_train_sets()
        self.adjust_scalers()

    def push_train_sets(self, train_x, train_y):
        self.train_x = train_x
        self.train_y = train_y

    def reshape_train_sets(self):
        self.train_x = reshaper(self.train_x)
        self.train_y = reshaper(self.train_y)

    def adjust_scalers(self):
        self.train_x = self.x_scaler.fit_transform(self.train_x)
        self.train_y = self.y_scaler.fit_transform(self.train_y)

    def setup_model(self):
        self.model.add(Dense(99, input_dim=1, activation='tanh', kernel_initializer='he_uniform'))
        self.model.add(Dense(256, activation='tanh', kernel_initializer='he_uniform'))
        self.model.add(Dense(90, activation='tanh', kernel_initializer='he_uniform'))
        self.model.add(Dense(45, activation='tanh', kernel_initializer='he_uniform'))
        self.model.add(Dense(20, activation='tanh', kernel_initializer='he_uniform'))
        self.model.add(Dense(10, activation='tanh', kernel_initializer='he_uniform'))
        self.model.add(Dense(1, activation='tanh', kernel_initializer='he_uniform'))

    def compile_model(self):
        self.model.compile(
            optimizer=keras.optimizers.Adam(),  # Optimizer
            loss=keras.losses.mean_squared_error,
            metrics=[
                keras.metrics.mean_squared_error,
                keras.metrics.mean_squared_logarithmic_error,
                keras.metrics.mean_absolute_percentage_error,
                keras.metrics.mean_absolute_error,
            ]
        )

    def fit_model(self, verbose=0):
        return self.model.fit(
            self.train_x[:int(len(self.train_x) * 0.66)],
            self.train_y[:int(len(self.train_x) * 0.66)],
            epochs=900,
            # steps_per_epoch=10,
            batch_size=10,
            verbose=verbose,
            validation_data=(self.train_y[int(len(self.train_x) * 0.66):],
                             self.train_x[int(len(self.train_x) * 0.66):])
        ).history

    def evaluate(self, x_test, y_test):
        return self.model.evaluate(x_test, y_test, batch_size=12, verbose=1)

    def predict(self, prediction_interval_x):
        prediction_interval_x = reshaper(prediction_interval_x)
        prediction_interval_x = self.x_scaler.transform(prediction_interval_x)
        predicted_y = self.model.predict(prediction_interval_x)

        self.x_plot = self.x_scaler.inverse_transform(self.train_x)
        self.y_plot = self.y_scaler.inverse_transform(self.train_y)
        self.x_pred_plot = self.x_scaler.inverse_transform(prediction_interval_x)
        self.y_pred_plot = self.y_scaler.inverse_transform(predicted_y)
        return self.y_pred_plot

    def visualize(self):
        pyplot.scatter(self.x_pred_plot, self.y_pred_plot, label='Predicted')
        pyplot.scatter(self.x_plot, self.y_plot, label='Actual')
        pyplot.title('Input (x) versus Output (y)')
        pyplot.xlabel('Input Variable (x)')
        pyplot.ylabel('Output Variable (y)')
        pyplot.legend()
        pyplot.show()
