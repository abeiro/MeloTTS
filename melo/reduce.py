import torch
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Process model checkpoint")
parser.add_argument('model_checkpoint2', type=str, help="Path to the second model checkpoint")
args = parser.parse_args()

# Load the original .pth checkpoint from the provided path
checkpoint_path = args.model_checkpoint2
checkpoint = torch.load(checkpoint_path)

# Keep only the model weights
model_state_dict = {}
model_state_dict['model'] = checkpoint['model']

# Save only the model weights to a new .pth file
output_path = "reduced_checkpoint.pth"
torch.save(model_state_dict, output_path)

print(f"Reduced checkpoint saved as '{output_path}'")
