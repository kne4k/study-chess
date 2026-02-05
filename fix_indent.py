with open(r'c:\Users\Leonardo CADS\Desktop\codes\study-xadrez\backend\chess\admin.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Remove 4 espaços de todas as linhas dentro do for (linhas 107-187)
new_lines = []
for i, line in enumerate(lines):
    line_num = i + 1
    if 107 <= line_num <= 187 and line.startswith('                '):
        # Remove 4 espaços
        new_lines.append(line[4:])
    else:
        new_lines.append(line)

with open(r'c:\Users\Leonardo CADS\Desktop\codes\study-xadrez\backend\chess\admin.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ Indentação corrigida!')
