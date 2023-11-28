"""Background Noise Generation Test Program

This program tests the background noise generation functionality of the Labsonar Synthesis library.
It generates background noise for various combinations of sea state, rain, and shipping noise levels.

"""
import os
import numpy as np
import scipy.io.wavfile as scipy_wav
import matplotlib.pyplot as plt

import labsonar_sp.analysis as sp_analysis
import labsonar_synthesis.background as syn_bg


def main():
    """Main function for the background noise generation test program."""
    
    # Set up the directory for saving results
    base_dir = "./result"
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)

    # Iterate over different combinations of sea state, rain, and shipping noise levels
    for shipping in [syn_bg.Shipping.NONE, syn_bg.Shipping.LEVEL_7]:
        for sea_state in [syn_bg.Sea.STATE_0, syn_bg.Sea.STATE_6]:
            for rain in [syn_bg.Rain.NONE, syn_bg.Rain.VERY_HEAVY]:

                # Define output file paths
                output_wav = f"{base_dir}/bg-{shipping}_{sea_state}_{rain}_audio.wav"
                output_png = f"{base_dir}/bg-{shipping}_{sea_state}_{rain}_spectrum.png"

                # Set parameters for noise generation
                fs = 48000
                n_samples = 100 * fs

                # Generate background noise and desired spectrum for comparison
                noise = syn_bg.generate_bg_noise(sea_state, rain, shipping, n_samples=n_samples, fs=fs)
                frequencies, desired_spectrum = syn_bg.generate_bg_spectrum(sea_state, rain, shipping, fs=fs)
                fft_freq, fft_result = syn_bg.estimate_spectrum(noise, n_samples/1000, overlap=0.5, fs=fs)

                # Plot and save the spectrum for comparison
                plt.figure(figsize=(12, 6))
                plt.plot(fft_freq, fft_result, label='Test Spectrum')
                plt.plot(frequencies, desired_spectrum, linestyle='--', label='Desired Spectrum')
                plt.xlabel('Frequency (Hz)')
                plt.ylabel('Amplitude (dB)')
                plt.legend()
                plt.savefig(output_png)
                plt.close()

                # Save the generated noise as a WAV file
                scipy_wav.write(output_wav, fs, sp_analysis.normalize(noise, 1))

    print(f"Output files generated in {base_dir}")


if __name__ == "__main__":
    main()
