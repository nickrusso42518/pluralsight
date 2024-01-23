#!/bin/bash
# Perform basic setup needed to interact with the AWS EKS cluster.

# Installs the "kubectl" binary to simplify interaction with the k8s cluster.
# Docs: https://kubernetes.io/docs/tasks/tools/install-kubectl/
# Or here: https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html
K=$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)
curl -LO https://storage.googleapis.com/kubernetes-release/release/"$K"/bin/linux/amd64/kubectl
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
kubectl version --short --client

# Installs the "aws-iam-authenticator" binary so kubectl can talk to AWS EKS
# Docs: https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html
curl -o aws-iam-authenticator \
  https://amazon-eks.s3-us-west-2.amazonaws.com/1.14.6/2019-08-22/bin/linux/amd64/aws-iam-authenticator
chmod +x aws-iam-authenticator
sudo mv aws-iam-authenticator /usr/local/bin/
aws-iam-authenticator version

# Ensure awscli can talk to AWS using the credentials in the Travis env vars,
# then set up the k8s using in AWS EKS
# Docs: https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html
aws sts get-caller-identity
aws eks update-kubeconfig --name globo_cluster
