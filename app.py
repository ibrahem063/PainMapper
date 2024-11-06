import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from flask import Flask, request, jsonify
import sys
import io

# تغيير الترميز إلى UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. تعريف المتغيرات الضبابية للمدخلات والمخرجات
Answer1 = ctrl.Antecedent(np.arange(0, 6, 1), 'Answer1')
Answer2 = ctrl.Antecedent(np.arange(0, 6, 1), 'Answer2')
Answer3 = ctrl.Antecedent(np.arange(0, 6, 1), 'Answer3')
output = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'output')

# 2. تحديد دوال الانتماء للمدخلات
for answer in [Answer1, Answer2, Answer3]:
    answer['mf1'] = fuzz.trimf(answer.universe, [-5, -2.5, 0])
    answer['mf2'] = fuzz.trimf(answer.universe, [0, 1.3, 2.5])
    answer['mf3'] = fuzz.trimf(answer.universe, [1.5, 2.5, 3.5])
    answer['mf4'] = fuzz.trimf(answer.universe, [2.6, 3.6, 4.5])
    answer['mf5'] = fuzz.trimf(answer.universe, [3.7, 5, 6.5])

# 3. تحديد دوال الانتماء للمخرجات
output['no_pain'] = fuzz.trimf(output.universe, [-2, -1, 0])
output['low'] = fuzz.trimf(output.universe, [-0.1111, 0.2222, 0.5556])
output['medium'] = fuzz.trimf(output.universe, [0.2222, 0.5556, 0.8889])
output['extrem'] = fuzz.trimf(output.universe, [0.6667, 1, 1.333])

# 4. إنشاء جميع القواعد الضبابية
rules = []
for i in range(1, 6):
    for j in range(1, 6):
        for k in range(1, 6):
            if i == j == k == 1:
                rules.append(ctrl.Rule(Answer1[f'mf{i}'] & Answer2[f'mf{j}'] & Answer3[f'mf{k}'], output['no_pain']))
            elif i <= 3 and j <= 3 and k <= 3:
                rules.append(ctrl.Rule(Answer1[f'mf{i}'] & Answer2[f'mf{j}'] & Answer3[f'mf{k}'], output['low']))
            elif i <= 4 and j <= 4 and k <= 4:
                rules.append(ctrl.Rule(Answer1[f'mf{i}'] & Answer2[f'mf{j}'] & Answer3[f'mf{k}'], output['medium']))
            else:
                rules.append(ctrl.Rule(Answer1[f'mf{i}'] & Answer2[f'mf{j}'] & Answer3[f'mf{k}'], output['extrem']))

# 5. تفعيل نظام التحكم الضبابي
control_system = ctrl.ControlSystem(rules)

# تعريف دالة لإعداد النظام الضبابي وتشغيله
def run_fuzzy_system(answer1, answer2, answer3, control_system, system_name):
    simulation = ctrl.ControlSystemSimulation(control_system)
    
    # ضبط القيم المدخلة
    simulation.input['Answer1'] = answer1
    simulation.input['Answer2'] = answer2
    simulation.input['Answer3'] = answer3
    
    # تنفيذ الحساب
    simulation.compute()
    output = simulation.output['output']
    
    # عرض النتيجة
    print(f"{system_name} المخرج:")
    print(output)
    return output

# إعداد التطبيق Flask
app = Flask(__name__)

@app.route('/fuzzy', methods=['POST'])
def fuzzy_logic():
    data = request.json
    answer1 = data.get('answer1')
    answer2 = data.get('answer2')
    answer3 = data.get('answer3')
    
    # تنفيذ المنطق الضبابي
    output = run_fuzzy_system(answer1, answer2, answer3, control_system, "System Name")
    return jsonify({'output': output})

@app.route('/')
def hello_world():
    return 'مرحبًا بالعالم!'

if __name__ == '__main__':
    app.run(debug=True)
