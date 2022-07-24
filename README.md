<p align="center">
	<img height="100" src="https://github.com/Fiber-Optic-Sensing-System/mpg-foss/blob/ca14cea3c6ce3d2d67e35d5f1deb7564991edfd2/data/images/a_logo.png"/>
</p>

<img alt="GitHub release (latest by date including pre-releases)" src="https://img.shields.io/github/v/release/Fiber-Optic-Sensing-System/mpg-foss?include_prereleases"> <a href="https://www.codacy.com/gh/Fiber-Optic-Sensing-System/mpg-foss/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Fiber-Optic-Sensing-System/mpg-foss&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/8e5195d53faf4b0ba11982536b1a41af"/></a>

## About

### This tool

**mpg-foss-α** is a Software tool used in the develpment of FOSS (fiber optic sensing systems) for applications by Carthage Space Sciences, WSGC, & NASA. Designed to interface with interrogator (gator) devices. This software is designed to interface with intrinsic fiber optic sensing technology, whereby the fiber optic cable itself is the sensor.

### Fiber optic sensing systems

>Fiber optic sensing systems (foss) use the physical properties of light as it travels along a fiber to detect changes in temperature, strain, and other parameters. There are, generally speaking, three generations of technologies: point fiber bragg grating (FBG) based sensors, scattering and spatially continuous FBG based. Scattering techniques take fully distributed measurements while FBG techniques can have a handful of sensing points or be fully distributed depending on how the system interprets the signal from the sensing element. FBGs act as miniscule mirrors and are manufactured into the core of the fiber. As light travels down the fiber, each grating reflects a portion of the signal back to the system. The system recognizes changes in the returning signal and interprets this information to provide accurate strain and temperature measurements. Below is a diagram pointing out the structure of an optical fiber, and the spectral response to an input.

<br>
<p align="center">
	<img height="500" src="https://github.com/Fiber-Optic-Sensing-System/mpg-foss/blob/c3c8e43dac2e40039a262d6b672838843d58e560/data/images/fbg_diagram.png"/>
</p>
<br>

### Benefits of the technology

>Strain gauges and thermocouples have long been the standard for measuring strain and temperature during testing.  While these technologies have been good enough for decades, they are not always able to effectively test and monitor the innovations of today. The limitations of legacy technology are not about accuracy, rather it is primarily about the level of insight provided by the data. Strain gauges and thermocouples only provide points of information, while some types of fiber optic sensors can provide spatially continuous data along the entire length of the fiber. As a result, engineers can measure strain fields and temperature distributions on a structure in order to better understand how the component behaves under different conditions. While point sensors only allow engineers to monitor critical points, distributed (spatially continuous data) sensors can measure what happens at critical points and everywhere in between. This level of insight is invaluable when it comes to designing with new composite materials. Additionally, fiber optic sensors can be embedded in materials in order to provide greater insight into the internal behavior of composite components and structures. 

## General usage
- **mpg-foss-α** requires at least **[Python 3.10.0](https://www.python.org/downloads/)**.

- Start by **[downloading](https://github.com/Fiber-Optic-Sensing-System/mpg-foss/archive/refs/heads/main.zip)** or `git clone`ing the source code.
  - *Extract the repo folder if you downloaded the main branch directly.*

- Use the `foss.py` script in the root directory to execute commands.
 	- `deps` gets required modules.
 	- `data` starts gator hardware data retrieval.
 	- `clean` removes parsed data *.csv* files.
 	- ~~`sim` starts usb gator data output simulation.~~
	- `help` to list commands.
	
- Invoke the foss.py script like you would any other Python script file.
  - e.g. `python foss.py wisdom`
	
- **mpg-foss-α** does not use Pipenv at the moment. Instead, there is a built in bootstrapper/update tool that should be invoked using `python foss.py deps`.
<br>

### Examples

<br>
<p align="center">
	<img height="240" src="https://github.com/Fiber-Optic-Sensing-System/mpg-foss/blob/c3c8e43dac2e40039a262d6b672838843d58e560/data/images/example_usage.png"/>
	<br>
	<img height="500" src="https://github.com/Fiber-Optic-Sensing-System/mpg-foss/blob/c3c8e43dac2e40039a262d6b672838843d58e560/data/images/example_data_collection.png"/>
	<img height="500" src="https://github.com/Fiber-Optic-Sensing-System/mpg-foss/blob/c3c8e43dac2e40039a262d6b672838843d58e560/data/images/example_csv.png"/>
	<br>
	<img height="350" src="https://github.com/Fiber-Optic-Sensing-System/mpg-foss/blob/c3c8e43dac2e40039a262d6b672838843d58e560/data/images/example_structure.png"/>
	<img height="250" src="https://github.com/Fiber-Optic-Sensing-System/mpg-foss/blob/c3c8e43dac2e40039a262d6b672838843d58e560/data/images/example_cleanup.png"/>	
</p>
<br>

## Notes

### Unit Conversion
The central wavelengths (CoG bit numbers) that are generated by Gator devices are absolute, calibrated central wavelengths in the operating range of the gator. To make full use of the available 18 bit register, the following conversion can be used to determine the actual central wavelength `λCW` in nm.

`$$ λ_{CW} = \frac{1514 + CoG_{bit}}{2^{18} * 72} $$`

In order to determine the strain `ε` or temperature change `ΔT` induced on an FBG sensor, one first has to know the default central wavelength value[^1] (unstrained / room Temperature) for the particular sensor, defined as λ0...  The relation between wavelength and strain and temperature is then as followed:

`$$\frac{\Delta\lambda}{\lambda_{0}}=\left( 1-\rho_e \right)\cdot \epsilon+\left( \alpha_\Lambda - \alpha_n \right)\bullet \Delta T$$`

Here `pe` is the strain-optic coefficient (0.22 for a glass fiber), `ε` the strain, `αΛ` the thermal expansion coefficient, αn thermo-optic coefficient and `ΔT` the induced temperature change.  For a bare glass fiber the temperature dependence `∆λ/ΔT` is typically in the order of 10 pm/°C at 1550 nm wavelength.

[^1]: The central wavelength and strain conversion are implemented in the software as options for the plots. 
