from system_monitor import get_system_metrics, log_metrics

def test_monitoring():
    # Test metrics collection
    print("Testing metrics collection...")
    metrics = get_system_metrics()
    print(f"Current metrics: {metrics}")
    
    # Test logging
    print("\nTesting logging functionality...")
    log_metrics(metrics)
    print("Check the logs folder for system_metrics.csv")

if __name__ == "__main__":
    test_monitoring()
