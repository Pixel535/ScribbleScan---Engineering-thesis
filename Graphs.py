import matplotlib.pyplot as plt

class Graphs:
    def __init__(self, logs_path):
        self.logs_path = logs_path
        self.create_graphs()

    def create_graphs(self):
        epoch = []
        loss = []
        CER = []
        WER = []
        val_loss = []
        val_CER = []
        val_WER = []

        with open(self.logs_path, 'r') as file:
            lines = file.readlines()

        for line in lines:

            if 'Epoch' not in line:
                continue

            elements = line.split(';')

            epoch_value = int(elements[0].split(' ')[-1])
            loss_value = float(elements[1].split(':')[-1])
            cer_value = float(elements[2].split(':')[-1])
            wer_value = float(elements[3].split(':')[-1])
            val_loss_value = float(elements[4].split(':')[-1])
            val_cer_value = float(elements[5].split(':')[-1])
            val_wer_value = float(elements[6].split(':')[-1])

            epoch.append(epoch_value)
            loss.append(loss_value)
            CER.append(cer_value)
            WER.append(wer_value)
            val_loss.append(val_loss_value)
            val_CER.append(val_cer_value)
            val_WER.append(val_wer_value)

        # Graphs
        plt.figure(figsize=(15, 10))

        # Loss and Epoch graph
        plt.subplot(2, 2, 1)
        plt.plot(epoch, loss, label='Train Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.title('Training Loss')
        plt.legend()

        # CER / WER and Epoch graph
        plt.subplot(2, 2, 2)
        plt.plot(epoch, CER, label='Train CER')
        plt.plot(epoch, WER, label='Train WER')
        plt.xlabel('Epoch')
        plt.ylabel('CER / WER')
        plt.title('Character Error Rate (CER) and Word Error Rate (WER)')
        plt.legend()

        # val_loss and Epoch graph
        plt.subplot(2, 2, 3)
        plt.plot(epoch, val_loss, label='Validation Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Validation Loss')
        plt.title('Validation Loss')
        plt.legend()

        # val_CER / val_WER and Epoch graph
        plt.subplot(2, 2, 4)
        plt.plot(epoch, val_CER, label='Validation CER')
        plt.plot(epoch, val_WER, label='Validation WER')
        plt.xlabel('Epoch')
        plt.ylabel('Validation CER / WER')
        plt.title('Validation Character Error Rate (CER) and Word Error Rate (WER)')
        plt.legend()

        # Show graphs
        plt.tight_layout()
        plt.show()