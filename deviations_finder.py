import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('--threshold', type=float, required=True, help='Deviation threshold')
parser.add_argument('--indexes', nargs='+', type=int, required=True, help='Indexes to compare (0-based)')
parser.add_argument('--input', type=str, default='deviations.txt', help='Input file')
parser.add_argument('--output', type=str, default='biggest_deviations.txt', help='Output file')
args = parser.parse_args()

filename = args.input
threshold = args.threshold
output_file = args.output
indexes = args.indexes

deviations = []
with open(filename, "r", encoding="utf-8") as f:
    for line in f:
        match = re.search(r"\[(.*?)\]", line)
        if match:
            nums = [int(x) for x in match.group(1).split(",")]
            for i in indexes:
                if i >= len(nums):
                    continue
                val = nums[i]
                rest = [nums[j] for j in range(len(nums)) if j != i and j in indexes]
                if not rest:
                    continue
                mean_rest = sum(rest) / len(rest)
                if abs(val - mean_rest) > threshold:
                    deviations.append(line.strip())
                    break

with open(output_file, "w", encoding="utf-8") as out:
    for line in deviations:
        out.write(line + "\n")
