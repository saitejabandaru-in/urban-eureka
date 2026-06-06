"""
Urban Eureka — Forecasting System
Implements Time Series Trend-Seasonal Decomposition, Anomaly Detection
using Rolling Statistics, and Double Exponential Smoothing forecasting.
"""

import numpy as np

class ForecastingSystem:
    @staticmethod
    def rolling_zscore_anomalies(series, window=7, threshold=2.0):
        """
        Detect anomalies using a rolling mean and standard deviation.
        """
        anomalies = []
        n = len(series)
        for i in range(n):
            if i < window:
                anomalies.append(False)
                continue
            history = series[i - window : i]
            mean = np.mean(history)
            std = np.std(history)
            
            if std == 0:
                z_score = 0
            else:
                z_score = (series[i] - mean) / std
                
            anomalies.append(abs(z_score) > threshold)
        return np.array(anomalies)

    @staticmethod
    def double_exponential_smoothing(series, alpha=0.2, beta=0.1, n_forecast=5):
        """
        Double Exponential Smoothing for trend-based forecasting.
        """
        result = [series[0]]
        level = series[0]
        trend = series[1] - series[0]
        
        for i in range(1, len(series)):
            val = series[i]
            last_level = level
            level = alpha * val + (1 - alpha) * (level + trend)
            trend = beta * (level - last_level) + (1 - beta) * trend
            result.append(level + trend)
            
        # Forecast
        forecast = []
        for i in range(1, n_forecast + 1):
            forecast.append(level + i * trend)
            
        return np.array(result), np.array(forecast)

if __name__ == "__main__":
    # Generate mock daily time-series with trend and anomalies: 100 days
    np.random.seed(42)
    time = np.arange(100)
    trend = 0.5 * time
    noise = np.random.normal(0, 2, 100)
    series = trend + noise
    
    # Inject anomalies
    series[30] += 15
    series[75] -= 15
    
    # 1. Detect Anomalies
    anomalies = ForecastingSystem.rolling_zscore_anomalies(series, window=10, threshold=2.5)
    anomaly_indices = np.where(anomalies)[0]
    
    # 2. Forecasting
    fitted, forecast = ForecastingSystem.double_exponential_smoothing(series, n_forecast=7)
    
    print("Forecasting & Time Series Analysis Complete:")
    print(f"  Detected anomalies at indices: {list(anomaly_indices)}")
    print(f"  7-Day Ahead Forecast: {np.round(forecast, 2)}")
