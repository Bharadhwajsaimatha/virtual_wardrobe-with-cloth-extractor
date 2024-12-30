# Virtual Wardrobe - An online trail room for your fashion needs

![Virtual Wardrobe](assets/demo.gif)

## Introduction

Virtual Wardrobe is an online trail room for your fashion needs. The project allows users to try on clothes and accessories virtually. Users can upload their image and try on different clothes and accessories. The application uses machine learning to detect the user's body and overlay the clothes and accessories on the user's body. Users can also save the images and share them with others.

## Features

- Upload Image: Users can upload their image and try on different clothes and accessories.
- Foreground Extraction: The project uses Gaussian Mixture Model (GMM) to extract the foreground from the background.
- Pose Detection: The project uses PoseNet to detect the user's body and pose.
- Overlay Clothes: The project overlays the clothes and accessories on the user's body.
- Save Image: Users can save the images and share them with others.
- A GUI is provided for easy interaction.

## Note

- The project is limited to overlaying upper body clothes and accessories.
- Executables are avaialble for Windows upon request.

## Installation

1. Clone the repository

```bash
git clone https://github.com/Bharadhwajsaimatha/virtual_wardrobe-with-foreground-extractor.git
```

2. Install the required packages

```bash
pip install -r requirements.txt
```

3. Run the application

- Demo extracted images can be found at `data/extracted_images`

```bash
python src/Virtual_wardrobe.py
```

- If you want to use the foreground extractor, run the following command

```bash
python src/Tee_extractor.py
```
## Contribution

Contributions are always welcome! Please create a pull request to contribute to the project.

## Contact

If you want to contact me you can reach me at [Email](mailto:bharadhwaj2299@gmail.com)

OR

[Portfolio](https://bharadhwajsaimatha.github.io/portfolio/)


## License

