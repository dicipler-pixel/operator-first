# SCRIPT: CHARLIE_STACK -- every verified line in the inbox, deduplicated, one per line, for the lunch hand-off
cd /home/claude/acc/charlie
cat runs/surgery_inbox/*.txt kernel/inbox/*.txt 2>/dev/null | grep -E '^s?ac-[0-9]+: \[' | sort -u > runs/STACK_charlie_for_lunch.txt
wc -l < runs/STACK_charlie_for_lunch.txt
