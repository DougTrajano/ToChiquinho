# SageMaker Custom DLC (Deep Learning Container)

This folder contains the code to build a custom DLC (Deep Learning Container) for SageMaker.

We are using a custom DLC to run our training and inference jobs. The custom DLC is based on the [PyTorch DLC]().

We extended the PyTorch DLC to include the additional python dependencies and [Git Large File Storage (LFS)](https://git-lfs.com/).

## References

- [Deep Learning Containers Images - AWS Deep Learning Containers](https://docs.aws.amazon.com/deep-learning-containers/latest/devguide/deep-learning-containers-images.html)
- [SageMaker Custom DLC](https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms.html)
- [Extending our PyTorch containers — Amazon SageMaker Examples 1.0.0 documentation](https://sagemaker-examples.readthedocs.io/en/latest/advanced_functionality/pytorch_extending_our_containers/pytorch_extending_our_containers.html)
- [aws/sagemaker-pytorch-training-toolkit](https://github.com/aws/sagemaker-pytorch-training-toolkit)
- [aws/deep-learning-containers/available_images.md](https://github.com/aws/deep-learning-containers/blob/master/available_images.md)