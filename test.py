from datetime import datetime, timedelta

def generate_schedule(num_shifts_per_day, start_date, end_date, num_employees):
    total_shifts = num_shifts_per_day * (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days
    shifts_per_employee = total_shifts // num_employees
    extra_shifts = total_shifts % num_employees

    employee_shifts = []
    for i in range(num_employees):
        num_shifts = shifts_per_employee
        if extra_shifts > 0:
            num_shifts += 1
            extra_shifts -= 1
        employee_shifts.append(num_shifts)

    schedule = {}
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    shift_index = 1
    
    while current_date <= datetime.strptime(end_date, '%Y-%m-%d'):
        for i in range(num_shifts_per_day):
            shift_key = f'Shift {shift_index}'
            schedule[shift_key] = []
            shift_index += 1
        
        for i in range(num_employees):
            for j in range(employee_shifts[i]):
                shift_key = f'Shift {j % num_shifts_per_day + 1}'
                employee_key = f'Employee {i + 1}'
                schedule[shift_key].append(employee_key)
                
        current_date += timedelta(days=1)
    
    return schedule

# Example usage
schedule = generate_schedule(2, '2023-05-01', '2023-05-07', 3)
print(schedule)
