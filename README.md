
# Diffusion Morphs (DiM)<br><sub>The official implementation of the 2024 IEEE TBIOM and 2024 IEEE S&P papers</sub>

![Teaser image](./docs/assets/dim_morph_comp.png)

**Leveraging Diffusion for Strong and High Quality Face Morphing Attacks**<br>
Zander W. Blasingame and Chen Liu<br>
[IEEE TBIOM](https://ieeexplore.ieee.org/document/10381591) [arXiv](https://arxiv.org/abs/2301.04218)

Abstract: *Face morphing attacks seek to deceive a Face Recognition (FR) system by presenting a morphed image consisting of the biometric qualities from two different identities with the aim of triggering a false acceptance with one of the two identities, thereby presenting a significant threat to biometric systems. The success of a morphing attack is dependent on the ability of the morphed image to represent the biometric characteristics of both identities that were used to create the image. We present a novel morphing attack that uses a Diffusion-based architecture to improve the visual fidelity of the image and the ability of the morphing attack to represent characteristics from both identities. We demonstrate the effectiveness of the proposed attack by evaluating its visual fidelity via the Frechet Inception Distance (FID). Also, extensive experiments are conducted to measure the vulnerability of FR systems to the proposed attack. The ability of a morphing attack detector to detect the proposed attack is measured and compared against two state-of-the-art GAN-based morphing attacks along with two Landmark-based attacks. Additionally, a novel metric to measure the relative strength between different morphing attacks is introduced and evaluated.*

**Fast-DiM: Towards Fast Diffusion Morphs**<br>
Zander W. Blasingame and Chen Liu<br>
[IEEE Security & Privacy](https://ieeexplore.ieee.org/document/10569993) [arXiv](https://arxiv.org/abs/2310.09484)

Abstract: *Diffusion Morphs (DiM) are a recent state-of-the-art method for creating high quality face morphs; however, they require a high number of network function evaluations (NFE) to create the morphs. We propose a new DiM pipeline, Fast-DiM, which can create morphs of a similar quality but with fewer NFE. We investigate the ODE solvers used to solve the Probability Flow ODE and the impact they have on the the creation of face morphs. Additionally, we employ an alternative method for encoding images into the latent space of the Diffusion model by solving the Probability Flow ODE as time runs forwards. Our experiments show that we can reduce the NFE by upwards of 85% in the encoding process while experiencing only 1.6\% reduction in Mated Morph Presentation Match Rate (MMPMR). Likewise, we showed we could cut NFE, in the sampling process, in half with only a maximal reduction of 0.23% in MMPMR.*

## Code Access
Sign the [code request form](CITeR_SoftwareReleaseAgreeement.docx) and send it to [citer@clarkson.edu](mailto:citer@clarkson.edu?subject=[GitHub]%20DiM%20Source%20Code%20Request)

 ## Citation
```bibtex
@article{blasingame_dim,
   title={Leveraging Diffusion for Strong and High Quality Face Morphing Attacks},
   volume={6},
   ISSN={2637-6407},
   url={http://dx.doi.org/10.1109/TBIOM.2024.3349857},
   DOI={10.1109/tbiom.2024.3349857},
   number={1},
   journal={IEEE Transactions on Biometrics, Behavior, and Identity Science},
   publisher={Institute of Electrical and Electronics Engineers (IEEE)},
   author={Blasingame, Zander W. and Liu, Chen},
   year={2024},
   month=jan, pages={118–131}}

@article{blasingame_fast_dim,
   title={Fast-DiM: Towards Fast Diffusion Morphs},
   volume={22},
   ISSN={1558-4046},
   url={http://dx.doi.org/10.1109/MSEC.2024.3410112},
   DOI={10.1109/msec.2024.3410112},
   number={4},
   journal={IEEE Security &amp; Privacy},
   publisher={Institute of Electrical and Electronics Engineers (IEEE)},
   author={Blasingame, Zander W. and Liu, Chen},
   year={2024},
   month=jul, pages={103–114} }
```
