import os
import json

# 获取所有非_results.json的JSON文件
files = [f for f in os.listdir('.') if f.endswith('.json') and not f.endswith('_results.json')]

# 按字母顺序排序文件名
files.sort()

print(f"找到{len(files)}个语言文件：{', '.join(files)}")
print("\n语言文件中问题数量统计：")
print("-" * 50)

# 统计每个文件中的问题数量
total_questions = 0
for file in files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            question_count = len(data)
            total_questions += question_count
            print(f"{file}: {question_count}个问题")
    except Exception as e:
        print(f"{file}: 读取出错 - {str(e)}")

print("-" * 50)
print(f"总计: {total_questions}个问题")
print(f"平均每个文件: {total_questions/len(files):.2f}个问题") 