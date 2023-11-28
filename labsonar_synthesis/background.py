"""Background Noise Generation Module

This module provides functionality to generate background noise based on different environmental conditions,
such as rain, sea state, and shipping noise. The noise is generated based on the frequency response data available in
Chapter 7 of "Underwater Acoustics: Analysis, Design, and Performance of SONAR" by R. P. Hodges (John Wiley and Sons, Ltd, 2010).


This module defines three Enums representing different sources of background noise:
- Rain: Enum for rain noise with various intensity levels.
- Sea: Enum for sea state noise with different states.
- Shipping: Enum for shipping noise with various intensity levels.

Each Enum provides methods to retrieve the corresponding frequency spectrum and generate noise.

"""
import os
import enum
import numpy as np
import pandas as pd
import scipy.signal as scipy


class Rain(enum.Enum):
    """Enum representing rain noise with various intensity levels."""
   
    NONE = 0
    LIGHT = 1 #(1 mm/h)
    MODERATE = 2 #(5 mm/h)
    HEAVY = 3 #(10 mm/h)
    VERY_HEAVY = 4 #(100 mm/h)
    
    @staticmethod
    def __get_csv() -> str:
        return os.path.join(os.path.dirname(__file__), "data", "rain.csv")

    def __str__(self):
        if self == Rain.NONE:
            return "without rain"
        return str(self.name).split('.')[-1].lower().replace("_", " ") + " rain"
    
    def get_spectrum(self) -> [np.array, np.array]:
        """Get the spectrum of the rain noise
        Returns:
            np.array: Frequencies in Hz.
            np.array: Estimate spectrum in dB ref 1μPa @1m/Hz.
        """
        df = pd.read_csv(Rain.__get_csv())
        frequencies = df[df.columns[0]].values
        if self != Rain.NONE:
            spectrum = df[df.columns[self.value]].values
        else:
            spectrum = np.zeros(frequencies.size)
        return frequencies, spectrum
    
    def get_noise(self, n_samples: int, fs: float) -> np.array:
        """Get the signal of the rain noise

        Args:
            n_samples (int): number of samples
            fs (float): sample frequency (Hz)

        Returns:
            np.array: Synthetic noise in μPa.
        """
        if self != Rain.NONE:
            frequencies, spectrum = self.get_spectrum()
            return generate_noise(frequencies, spectrum, n_samples, fs)
        return np.zeros(n_samples)


class Sea(enum.Enum):
    STATE_0 = 0
    STATE_1 = 1
    STATE_2 = 2
    STATE_3 = 3
    STATE_4 = 4
    STATE_5 = 5
    STATE_6 = 6

    @staticmethod
    def __get_csv() -> str:
        return os.path.join(os.path.dirname(__file__), "data", "sea_state.csv")
    
    def __str__(self):
        return f"sea state {self.value}"

    def get_spectrum(self) -> [np.array, np.array]:
        """Get the spectrum of the sea state
        Returns:
            np.array: Frequencies in Hz.
            np.array: Estimate spectrum in dB ref 1μPa @1m/Hz.
        """
        df = pd.read_csv(Sea.__get_csv())
        frequencies = df[df.columns[0]].values
        spectrum = df[df.columns[self.value + 1]].values
        return frequencies, spectrum

    def get_noise(self, n_samples: int, fs: float) -> np.array:
        """Get the signal of the sea state

        Args:
            n_samples (int): number of samples
            fs (float): sample frequency (Hz)

        Returns:
            np.array: Synthetic noise in μPa.
        """
        frequencies, spectrum = self.get_spectrum()
        return generate_noise(frequencies, spectrum, n_samples, fs)


class Shipping(enum.Enum):
    NONE = 0
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4
    LEVEL_5 = 5
    LEVEL_6 = 6
    LEVEL_7 = 7

    @staticmethod
    def __get_csv() -> str:
        return os.path.join(os.path.dirname(__file__), "data", "shipping_noise.csv")
    
    def __str__(self):
        if self == Shipping.NONE:
            return "without shipping noise"
        return "shipping noise " + str(self.name).split('.')[-1].lower().replace("_", " ")

    def get_spectrum(self) -> [np.array, np.array]:
        """Get the spectrum of the shipping noise
        Returns:
            np.array: Frequencies in Hz.
            np.array: Estimate spectrum in dB ref 1μPa @1m/Hz.
        """
        df = pd.read_csv(Shipping.__get_csv())
        frequencies = df[df.columns[0]].values        
        if self != Shipping.NONE:
            spectrum = df[df.columns[self.value]].values
        else:
            spectrum = np.zeros(frequencies.size)
        return frequencies, spectrum

    def get_noise(self, n_samples: int, fs: float) -> np.array:
        """Get the signal of the shipping noise

        Args:
            n_samples (int): number of samples
            fs (float): sample frequency (Hz)

        Returns:
            np.array: Synthetic noise in μPa.
        """
        if self != Shipping.NONE:
            frequencies, spectrum = self.get_spectrum()
            return generate_noise(frequencies, spectrum, n_samples, fs)
        return np.zeros(n_samples)


def generate_noise(frequencies: np.array, intensities: np.array, n_samples: int, fs: float) -> np.array:
    """Generate background noise based on frequency and intensity information.

    Args:
        frequencies (np.array): Array of frequency values.
        intensities (np.array): Array of intensity values in dB ref 1μPa @1m/Hz.
        n_samples (int): Number of samples to generate.
        fs (float): Sampling frequency.

    Returns:
        np.array: Generated background noise in μPa.

    Raises:
        UnboundLocalError: Raised if frequencies and intensities have different lengths.

    """

    if len(frequencies) != len(intensities):
        raise UnboundLocalError("for generate_noise frequencies and intensities must have the same length")

    # garantindo que as frequências inseridas contenham as frequência 0 e fs/2 (exigido pela scipy.firwin2)
    #   e estejam limitadas ao critério de nyquist
    index = np.argmax(frequencies > (fs/2.0))
    if index > 0:
        if frequencies[index-1] == (fs/2):
            frequencies = frequencies[:index]
            intensities = intensities[:index]
        else:
            f = fs/2
            i = intensities[index-1] + (intensities[index]-intensities[index-1])*(f-frequencies[index-1])/(frequencies[index]-frequencies[index-1])
            
            frequencies = np.append(frequencies[:index], f)
            intensities = np.append(intensities[:index], i)
    else:
        if frequencies[-1] != (fs/2):
            f = fs/2
            i = intensities[-1] + (intensities[-1]-intensities[-2])*(f-frequencies[-2])/(frequencies[-1]-frequencies[-2])

            frequencies = np.append(frequencies, f)
            intensities = np.append(intensities, i)

    if frequencies[0] != 0:
            frequencies = np.append(0, frequencies)
            intensities = np.append(intensities[0], intensities)

    # normalizando frequências entre 0 e 1
    if np.max(frequencies) > 1:
        frequencies = frequencies/(fs/2)

    order = 1025
    noise = np.random.normal(0, 1.13, n_samples + order)
    # 1.13 ajustado manualmente com base na aplicação de teste generate_noise.py para compensar um offset
    # gerando mais amostras que o desejado para eliminar a resposta transiente do filtro

    intensities = 10 ** ((intensities) / 20)

    coeficient = scipy.firwin2(order, frequencies, intensities, antisymmetric=False)
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.firwin2.html
    # antisymmetric=False, order=odd
    # filtro tipo 1 para que as frequências fs/2 e 0 não tenham que ser 0
    out_noise = scipy.lfilter(coeficient, 1, noise)
    return out_noise[order:]

def generate_bg_noise(sea: Sea, rain: Rain = Rain.NONE, shipping: Shipping = Shipping.NONE, n_samples: int = 1024, fs: float = 48000) -> np.array:
    """Generate background noise by combining sea state, rain and shipping noise.

    Args:
        sea (Sea): Enum representing sea state conditions.
        rain (Rain): Enum representing rain conditions.
        shipping (Shipping): Enum representing shipping noise conditions.
        n_samples (int): Number of samples to generate.
        fs (float): Sampling frequency.

    Returns:
        np.array: Combined background noise in μPa.

    """
    return sea.get_noise(n_samples, fs) + rain.get_noise(n_samples, fs) + shipping.get_noise(n_samples, fs)

def generate_bg_spectrum(sea: Sea, rain: Rain = Rain.NONE, shipping: Shipping = Shipping.NONE, fs: float = 48000) -> np.array:
    """Generate the combined frequency spectrum of rain and sea state.

    Args:
        sea (Sea): Enum representing sea state conditions.
        rain (Rain): Enum representing rain conditions.
        shipping (Shipping): Enum representing shipping noise conditions.
        fs (float): Sampling frequency.

    Returns:
        np.array: Combined frequency spectrum in dB ref 1μPa @1m/Hz.

    """

    # Calculando o espectro para cada condição
    frequencies1, spectrum1 = rain.get_spectrum()
    frequencies2, spectrum2 = sea.get_spectrum()
    frequencies3, spectrum3 = shipping.get_spectrum()

    # Calculando o espectro interpolado para compatibilização das frequencias entre os dados
    all_frequencies = np.unique(np.concatenate([frequencies1, frequencies2, frequencies3]))

    # Limitando o espectro seguindo critério de nyquist
    index = np.argmax(all_frequencies > (fs/2.0))
    if index > 0:
        all_frequencies = all_frequencies[:index]

    interpolated_spectrum1 = np.interp(all_frequencies, frequencies1, spectrum1, left=0, right=0)
    interpolated_spectrum2 = np.interp(all_frequencies, frequencies2, spectrum2, left=0, right=0)
    interpolated_spectrum3 = np.interp(all_frequencies, frequencies3, spectrum3, left=0, right=0)

    # Calculando a soma linear das intensidade
    linear1 = 10**(interpolated_spectrum1 / 20)
    linear2 = 10**(interpolated_spectrum2 / 20)
    linear3 = 10**(interpolated_spectrum3 / 20)
    interpolated_spectrum = 20 * np.log10(linear1 + linear2 + linear3)

    return all_frequencies, interpolated_spectrum

def estimate_spectrum(signal: np.array, window_size: int = 1024, overlap: float = 0.5, fs: float = 48000) -> [np.array, np.array]:
    """Estimate the medium spectrum based on data.

    Args:
        signal (np.array): data in 1μPa.
        window_size (int): fft window size.
        overlap (float): overlap fft window, between 0 and 1.
        fs (float): Sampling frequency.

    Returns:
        np.array: Frequencies in Hz.
        np.array: Estimate spectrum in dB ref 1μPa @1m/Hz.
    """

    if overlap == 1:
        raise UnboundLocalError("Overlap cannot be 1")

    window_size = int(window_size)
    n_samples = signal.size
    novity_samples = int(window_size * (1-overlap))

    fft_result = np.zeros(window_size//2)
    fft_freq = np.fft.fftfreq(window_size, 1/fs)[:window_size//2]

    i=0
    n_means = 0
    while i + novity_samples + window_size <= n_samples:
        fft_result = fft_result + np.abs(np.fft.fft(
                    signal[i:i+window_size], norm='ortho')
                [:window_size//2])
        i += novity_samples
        n_means += 1

    fft_result = fft_result/n_means
    fft_result = 20 * np.log10(fft_result)

    return fft_freq, fft_result
