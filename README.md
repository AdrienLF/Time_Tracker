<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** AdrienLF, Time_Tracker, NEOkeitaro, adrienlefalher.pro [at] gmail.com, Time Tracker, Time Tracker is a simple web interface based on Dash and Plotly, using NFC and a phone to do a simple time tracker.
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  
  <h3 align="center">Time Tracker</h3>

  <p align="center">
    Time Tracker is a simple web interface based on Dash and Plotly, using NFC and a phone to do a simple time tracker.
    <br />
    <a href="https://github.com/AdrienLF/Time_Tracker"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/AdrienLF/Time_Tracker">View Demo</a>
    ·
    <a href="https://github.com/AdrienLF/Time_Tracker/issues">Report Bug</a>
    ·
    <a href="https://github.com/AdrienLF/Time_Tracker/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://github.com/AdrienLF/Time_Tracker/blob/master/Time-Tracker_preview.jpg)

The iPhone's automation opens up many interesting workflows, especially since it can scan NFC chips. They are cheap, small, and are very easy to program. Many people have their phone with them all the time, so it seems like a natural ally to your time tracking obsession.

It works in two steps: on your phone, you have one automation per task/NFC chip. It will update a file on dropbox, which will sync to your computer. Then, this software will allow you to see the results in a more beautiful and useful way.  

### Built With

* [Python 3.7](https://www.python.org/)
* [Plotly](https://plotly.com/python/)
* [Dash](https://plotly.com/dash/open-source/)
* [Iphone Automations](https://support.apple.com/fr-fr/guide/shortcuts/apd602971e63/ios)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.


### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/AdrienLF/Time_Tracker.git
   ```
2. Install pip packages
   ```sh
   pip install -r requirements.txt
   ```



<!-- USAGE EXAMPLES -->
## Usage

The first thing you need to do is create the automations with your phone and NFC tags. The text must me as follows : 

```sh
Current Date (all ISO 8601) - Longitude/Latitude - Name of your activity
```

Don't forget the spaces around the "-". You can add as many automations as you like, and name them as you like. 

You also don't need NFCs for all of them. It could trigger when you leave home, receive e-mails, etc.

Then, replace the path to your file in the Main.py file. I use dropbox, you can use any service that syncs your file from your phone to your computer. 

![product-screenshot]](https://github.com/AdrienLF/Time_Tracker/blob/master/Screenshots/Change%20path.png?raw=true)

Then, run Main.py and open [http://127.0.0.1:8050/](http://127.0.0.1:8050/) on your browser.


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/AdrienLF/Time_Tracker/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Adrien Le Falher - [@NEOkeitaro](https://twitter.com/NEOkeitaro) - adrienlefalher.pro [at] gmail.com

Project Link: [https://github.com/AdrienLF/Time_Tracker](https://github.com/AdrienLF/Time_Tracker)






<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/AdrienLF/repo.svg?style=for-the-badge
[contributors-url]: https://github.com/AdrienLF/repo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/AdrienLF/repo.svg?style=for-the-badge
[forks-url]: https://github.com/AdrienLF/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/AdrienLF/repo.svg?style=for-the-badge
[stars-url]: https://github.com/AdrienLF/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/AdrienLF/repo.svg?style=for-the-badge
[issues-url]: https://github.com/AdrienLF/repo/issues
[license-shield]: https://img.shields.io/github/license/AdrienLF/repo.svg?style=for-the-badge
[license-url]: https://github.com/AdrienLF/Time_Tracker/blob/master/LICENSE.md
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/AdrienLF
