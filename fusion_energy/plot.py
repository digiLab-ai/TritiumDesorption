from matplotlib import rcParams
from matplotlib import pyplot as plt

# rcParams['figure.dpi'] = 200s
rcParams['font.family'] = 'Exo 2'


def style_axes(*axs):
    for ax in axs:
        for spine in ax.spines:
            ax.spines[spine].set_visible(False)
    ax.grid(True, which='major', axis='both', alpha=0.3)
    

def plot_test(i, test_data, mean, std, temperatures):

    mean_i = mean.iloc[i].values
    std_i = std.iloc[i].values
    test_i = test_data.iloc[i,5::].values

    text = "\n".join([
        f"{_input} = {_value:.2f}" if "E" in _input 
        else f"{_input} = {_value:.2E}"
        for j, (_input, _value) 
        in enumerate(zip(test_data.columns[:5],test_data.iloc[i,:5]))
    ]) 

    fig = plt.figure(figsize=(8,6))
    ax = plt.gca()

    plt.text(0.02, .98,text  , ha='left', va='top', transform=ax.transAxes)


    plt.plot(temperatures.values[0,::5], test_i[::5],'x',color="tab:red", label='Test data')
    plt.plot(temperatures.values[0,::5], mean_i[::5],color='tab:blue', label='GP Prediction')

    plt.fill_between(temperatures.values[0], mean_i - 2 * std_i, mean_i + 2 * std_i, alpha = 0.4, color='tab:blue')
    

    plt.title("Tritium Thermo-Desorption Spectra")
    plt.ylabel("Tritium Desorption Rate ")
    plt.xlabel("Temperature $(K)$")
    plt.legend()

    

