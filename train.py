import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from models.decision_tree import train_decision_tree
from models.dnn import train_dnn
from models.knn import train_knn
from models.naive_bayes import train_gaussian_nb
from models.random_forest import train_random_forest, train_improved_random_forest
from utils.file import get_top_n

class Training:
    def __init__(self, top_n_list, top_n_path='data', random_seed=3):
        self.top_n_list = top_n_list
        self.top_n_path = top_n_path
        self.random_seed = random_seed
        
        # Store results for plotting
        self.results_df = pd.DataFrame()
        
        self.dataset = self.read_dataset()
        self.best_classifier_list = self.training()
        self.best_classifier, self.best_accuracy, self.best_n = self.get_best_classifier()
        self.print_result()
        self.improved_model()
        self.plot_results()

    def read_dataset(self):
        """Read the dataset using the get_top_n function."""
        return get_top_n(self.top_n_path, self.top_n_list)

    def shuffle(self, array):
        """Shuffle the dataset with a fixed random seed."""
        np.random.seed(self.random_seed)
        np.random.shuffle(array)

    def training(self):
        best_classifier_all = []
        results_data = []
        
        for n, dataset_path in self.dataset:
            dataframe = pd.read_csv(dataset_path, index_col=False)
            dataset = dataframe.to_numpy()
            self.shuffle(dataset)

            fold = 6
            x_train = dataset[:, :-1]
            y_train = dataset[:, -1]
            print(f"Top: {n} Genes")
            print(f"Cross-validation fold: {fold}")
            print("-------------------------------")
            
            # Get scores for all models
            score_nb = train_gaussian_nb(x_train, y_train, fold)
            score_dt = train_decision_tree(x_train, y_train, fold)
            score_dnn = train_dnn(x_train, y_train, fold)
            score_rf = train_random_forest(x_train, y_train, fold)
            score_knn_2, score_knn_3, score_knn_4 = train_knn(x_train, y_train, [2, 3, 4], fold)
            
            # Store results for plotting
            results_data.append({
                'n_genes': n,
                'Naive Bayes': score_nb,
                'Decision Tree': score_dt,
                'Neural Network': score_dnn,
                'Random Forest': score_rf,
                'KNN (k=2)': score_knn_2,
                'KNN (k=3)': score_knn_3,
                'KNN (k=4)': score_knn_4
            })
            
            score_list = np.array([score_nb, score_dt, score_dnn, score_rf, score_knn_2, score_knn_3, score_knn_4])
            max_acc = np.max(score_list)
            best_classifier_idx = np.where(score_list == max_acc)
            best_classifier = self.find_best_classifier(best_classifier_idx[0])
            best_classifier_all.append([best_classifier, max_acc, n])
            print(f"Maximum accuracy: {max_acc:0.4f}")
            print("\n\n")
            print("-------------------------------")
        
        # Convert results to DataFrame for easier plotting
        self.results_df = pd.DataFrame(results_data)
        return best_classifier_all

    @staticmethod
    def find_best_classifier(index):
        """Find and return the name of the best classifier based on index."""
        if index == 0:
            print("Best classifier: Naive Bayes")
            return "Naive Bayes"
        elif index == 1:
            print("Best classifier: Decision tree")
            return "Decision Tree"
        elif index == 2:
            print("Best classifier: Neural Network")
            return "Neural Network"
        elif index == 3:
            print("Best classifier: Random Forest")
            return "Random Forest"
        elif index == 4:
            print("Best classifier: KNN with 2 neighbor")
            return "KNN with 2 neighbor"
        elif index == 5:
            print("Best classifier: KNN with 3 neighbor")
            return "KNN with 3 neighbor"
        elif index == 6:
            print("Best classifier: KNN with 4 neighbor")
            return "KNN with 4 neighbor"

    def get_best_classifier(self):
        """Get the best performing classifier overall."""
        sorted_list = sorted(self.best_classifier_list, key=lambda x: x[1], reverse=True)
        return sorted_list[0][:3]

    def print_result(self):
        """Print the results of the best classifier."""
        print(f"\n\n************************\n"
              f"Best classifier of the all training is:\n"
              f"\t{self.best_classifier}\n"
              f"Accuracy of the classifier is:\n"
              f"\t{self.best_accuracy}\n"
              f"Best top gene set is:\n"
              f"\t{self.best_n}\n"
              f"************************\n")

    def improved_model(self):
        """Train and evaluate the improved random forest model."""
        dataframe = pd.read_csv(self.dataset[-1][1], index_col=False)
        dataset = dataframe.to_numpy()
        self.shuffle(dataset)

        fold = 6
        x_train = dataset[:, :-1]
        y_train = dataset[:, -1]

        score_rf_imp = train_improved_random_forest(x_train, y_train, fold)

        print(f"\n\n************************\n"
              f"Accuracy of the improved classifier is:\n"
              f"\t{score_rf_imp}\n"
              f"************************\n")

    def plot_results(self):
        """Create and save visualization plots."""
        # Set the style
        sns.set_style("whitegrid")
        plt.figure(figsize=(12, 8))
        
        # Plot accuracy vs number of genes for all models
        for column in self.results_df.columns:
            if column != 'n_genes':
                plt.plot(self.results_df['n_genes'], self.results_df[column], marker='o', label=column)
        
        plt.xlabel('Number of Genes')
        plt.ylabel('Accuracy')
        plt.title('Model Accuracy vs Number of Genes')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig('graphs/accuracy_vs_genes.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Create a heatmap of model performances
        plt.figure(figsize=(10, 8))
        performance_matrix = self.results_df.drop('n_genes', axis=1).T
        performance_matrix.columns = self.results_df['n_genes']
        sns.heatmap(performance_matrix, annot=True, cmap='YlOrRd', fmt='.3f')
        plt.xlabel('Number of Genes')
        plt.ylabel('Model')
        plt.title('Model Performance Heatmap')
        plt.tight_layout()
        plt.savefig('graphs/performance_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Box plot of model performances
        plt.figure(figsize=(12, 6))
        model_data = self.results_df.drop('n_genes', axis=1).melt()
        sns.boxplot(x='variable', y='value', data=model_data)
        plt.xticks(rotation=45)
        plt.xlabel('Model')
        plt.ylabel('Accuracy')
        plt.title('Distribution of Model Performances')
        plt.tight_layout()
        plt.savefig('graphs/model_performance_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()

if __name__ == '__main__':
    tr = Training([2, 4, 6, 8, 10, 12, 15, 20, 25, 30])