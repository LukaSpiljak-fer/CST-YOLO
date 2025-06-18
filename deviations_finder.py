import re

filename = "deviations.txt"
threshold = 8  # Change this value for more/less sensitivity
output_file = "biggest_deviations.txt"

deviations = []
with open(filename, "r", encoding="utf-8") as f:
    for line in f:
        match = re.search(r"\[(.*?)\]", line)
        if match:
            nums = [int(x) for x in match.group(1).split(",")]
            for i, val in enumerate(nums):
                rest = nums[:i] + nums[i+1:]
                if not rest:
                    continue
                mean_rest = sum(rest) / len(rest)
                if abs(val - mean_rest) > threshold:
                    deviations.append(line.strip())
                    break

with open(output_file, "w", encoding="utf-8") as out:
    for line in deviations:
        out.write(line + "\n")
