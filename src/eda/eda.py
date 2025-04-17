import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_eda(df: pd.DataFrame, report_dir: str):
    """
    Generate and save EDA artifacts: histograms, correlation matrix, etc.
    """
    os.makedirs(report_dir, exist_ok=True)

    # Example: distribution of target
    plt.figure(figsize=(6,4))
    sns.countplot(x='Delay', data=df)
    plt.title('Delay Distribution')
    plt.savefig(os.path.join(report_dir, 'delay_dist.png'))
    plt.close()

    # Example: basic stats
    df.describe().to_csv(os.path.join(report_dir, 'summary_stats.csv'))
    
    # … add more plots / tables as in your notebook …