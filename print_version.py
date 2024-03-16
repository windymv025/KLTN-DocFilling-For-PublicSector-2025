import pkg_resources
# version = pkg_resources.get_distribution("langchain").version

print("langchain=="+ pkg_resources.get_distribution("langchain").version)
print("huggingface-hub=="+ pkg_resources.get_distribution("huggingface-hub").version)
print("langchain-community=="+ pkg_resources.get_distribution("langchain-community").version)
print("langchain-core=="+ pkg_resources.get_distribution("langchain-core").version)
print("python-dotenv=="+ pkg_resources.get_distribution("python-dotenv").version)
print("chainlit=="+ pkg_resources.get_distribution("chainlit").version)
print("chromadb=="+ pkg_resources.get_distribution("chromadb").version)
print("transformers=="+ pkg_resources.get_distribution("transformers").version)