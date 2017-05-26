from classifier.util import data_util
import matplotlib.pyplot as plt


if __name__ == '__main__':
    df = data_util._load_data('edwin')
    activities = df['activity'].unique()

    for a in activities:
        data = df[df.activity == a]
        if a == 'sitting':
            print(data)

        energy_ax = data['sp_energy_ax'].values
        energy_ay = data['sp_energy_ay'].values
        energy_az = data['sp_energy_az'].values
        energy_mag = data['sp_energy_acc_magnitude'].values

        x = [i for i in range(0, len(energy_ax))]
        plt.scatter(x, energy_ax, s=0.1, label='ax')
        plt.scatter(x, energy_ay, s=0.1, label='ay')
        plt.scatter(x, energy_az, s=0.1, label='az')
        plt.scatter(x, energy_mag, s=0.1, label='amag')
        plt.title(a)
        plt.legend()
        plt.ylim(-20, 20)
        plt.show()