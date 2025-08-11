import pandas as pd

# Load CSV
df = pd.read_csv("combined_results_with_iptm.csv")

# 1. Overall averages
avg_before = df["lrmsd_before"].mean()
avg_after = df["lrmsd_after"].mean()

# 2. First 20 rows
avg_before_first20 = df.head(20)["lrmsd_before"].mean()

# 3. Top 20 by lrmsd_after_rank
avg_after_top20_after_rank = df.sort_values("lrmsd_after_rank").head(20)["lrmsd_after"].mean()

# 4. Top 10 by score_rank
top10_score = df.sort_values("score_rank").head(10)
avg_before_top10_score = top10_score["lrmsd_before"].mean()
avg_after_top10_score = top10_score["lrmsd_after"].mean()

# 5. Top 10 by conf_score_rank
top10_conf = df.sort_values("conf_score_rank").head(10)
avg_before_top10_conf = top10_conf["lrmsd_before"].mean()
avg_after_top10_conf = top10_conf["lrmsd_after"].mean()

# Print summary
print("===== RMSD Statistics Summary =====")
print(f"Overall average lrmsd_before: {avg_before:.4f}")
print(f"Overall average lrmsd_after:  {avg_after:.4f}")
print()
print(f"Average lrmsd_before (first 20 rows): {avg_before_first20:.4f}")
print()
print(f"Average lrmsd_after (top 20 by lrmsd_after_rank): {avg_after_top20_after_rank:.4f}")
print()
print(f"Average lrmsd_before (top 10 by score_rank): {avg_before_top10_score:.4f}")
print(f"Average lrmsd_after  (top 10 by score_rank): {avg_after_top10_score:.4f}")
print()
print(f"Average lrmsd_before (top 10 by conf_score_rank): {avg_before_top10_conf:.4f}")
print(f"Average lrmsd_after  (top 10 by conf_score_rank): {avg_after_top10_conf:.4f}")
