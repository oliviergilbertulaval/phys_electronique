import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def get_values_from_file(filename):
    values = pd.read_csv(filename, delimiter="\t", decimal=",", skiprows=21)
    return values



def create_scatter(x_values, y_values, title="Title"):
    ax1 = plt.subplot(111)
    ticklabels = ax1.get_xticklabels()
    ticklabels.extend( ax1.get_yticklabels() )
    for label in ticklabels:
        label.set_fontsize(10)
    plt.plot(x_values, y_values, "o", color='blue')
    plt.suptitle(f'{title}', size=17)
    plt.ylabel(r'Intensité du courant [A]', size=17)
    plt.xlabel(r'Différence de potentiel [V]', size=17)
    plt.savefig(r'C:\Users\olivi\Desktop\Devoirs\PhysElectronique\figures\lab3'+f"\{title}.pdf", format="pdf", bbox_inches="tight")
    plt.show()

def create_multiple(x_values, y_values, title="Title"):
    ax1 = plt.subplot(111)
    ticklabels = ax1.get_xticklabels()
    ticklabels.extend( ax1.get_yticklabels() )
    for label in ticklabels:
        label.set_fontsize(10)
    for i in range(len(x_values)):
        plt.plot(x_values[i], y_values[i], "-", label=f"Tension base: {str(i*0.2)[:3]} V")
    plt.axvline(1)
    plt.text(2, 0.45, r"$i_\mathrm{sat}=0.5$A", fontsize=16)
    plt.legend()
    plt.suptitle(f'{title}', size=17)
    plt.ylabel(r'Intensité du courant [A]', size=17)
    plt.xlabel(r'Différence de potentiel [V]', size=17)
    plt.savefig(r'C:\Users\olivi\Desktop\Devoirs\PhysElectronique\figures\lab3'+f"\{title}.pdf", format="pdf", bbox_inches="tight")
    plt.show()







#diodes:
val = get_values_from_file("lab3/diode_polarise_directe.lvm")
tension1 = []
courant1 = []
for i in range(np.array(val).shape[0]):
    tension1.append(np.array(val)[:, 1:2][i][0])
    courant1.append(np.array(val)[:, 2:3][i][0])
#create_scatter(tension1, courant1, "Courbe $i-v$ de la diode en polarisation directe")

val = get_values_from_file("lab3/diode_polarite_inverse.lvm")
tension2 = []
courant2 = []
for i in range(np.array(val).shape[0]):
    tension2.append(np.array(val)[:, 1:2][i][0])
    courant2.append(np.array(val)[:, 2:3][i][0])
#create_scatter(tension2, courant2, "Courbe $i-v$ de la diode en polarisation inverse")

val = get_values_from_file("lab3/diode_zener.lvm")
tension = []
courant = []
for i in range(np.array(val).shape[0]):
    tension.append(np.array(val)[:, 1:2][i][0])
    courant.append(np.array(val)[:, 2:3][i][0])
#create_scatter(tension, courant, "Courbe $i-v$ de la diode Zener")



#Résistance dynamique:
resistance = []
for i in range(len(tension1)-1):
    resistance.append((tension1[i+1]-tension1[i])/(courant1[i+1]-courant1[i]))
resistance2 = []
for i in range(len(tension2)-1):
    resistance2.append((tension2[i+1]-tension2[i])/(courant2[i+1]-courant2[i]))


ax1 = plt.subplot(111)
ticklabels = ax1.get_xticklabels()
ticklabels.extend( ax1.get_yticklabels() )
for label in ticklabels:
    label.set_fontsize(10)
plt.plot(tension1[:-1], resistance, "o", label="polarisation directe")
#plt.plot(tension2[:-1], resistance2, "o", label="polarisation inverse")
plt.suptitle(f'Résistance dynamique mesurée en fonction de la tension', size=17)
#plt.legend()
plt.ylabel(r'$R_D$ [$\Omega$]', size=17)
plt.xlabel(r'Différence de potentiel [V]', size=17)
plt.savefig(r'C:\Users\olivi\Desktop\Devoirs\PhysElectronique\figures\lab3'+f"\$ressitance$.pdf", format="pdf", bbox_inches="tight")
plt.show()


def shockley(v, i_0, v_0):
    return i_0*(np.exp(v/v_0)-1)

from scipy.optimize import curve_fit

res = curve_fit(shockley, tension1, courant1)[0]

print(res)

x_data = np.linspace(0, 1, 100)

ax1 = plt.subplot(111)
ticklabels = ax1.get_xticklabels()
ticklabels.extend( ax1.get_yticklabels() )
for label in ticklabels:
    label.set_fontsize(10)
plt.plot(tension1, courant1, "o", label="données")
plt.plot(x_data, shockley(x_data, res[0], res[1]), "-", label="shockley")
#plt.plot(x_data, shockley(x_data, 1e-05, 0.12), "-", label="manuel")
plt.legend()
plt.suptitle(r'Courbe $i-v$ ajustée avec Shockley', size=17)
plt.ylabel(r'Intensité du courant [A]', size=17)
plt.xlabel(r'Différence de potentiel [V]', size=17)
plt.savefig(r'C:\Users\olivi\Desktop\Devoirs\PhysElectronique\figures\lab3'+f"\$Shockley_fit$.pdf", format="pdf", bbox_inches="tight")
plt.show()