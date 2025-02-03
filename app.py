import mysql.connector
import psutil
import platform
import socket
import datetime
import GPUtil
from flask import Flask, render_template

app = Flask(__name__)

# MySQL Database Connection
def get_db_connection():
    return mysql.connector.connect(
       'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
    )

def calculate_user_recipe_space():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Fetch table-level size and row count
    cursor.execute("""
        SELECT 
            ROUND(data_length / 1024, 2) AS DataSize_KB,
            ROUND(index_length / 1024, 2) AS IndexSize_KB,
            ROUND((data_length + index_length) / 1024, 2) AS TotalSize_KB,
            ROUND((data_length + index_length) / (1024 * 1024), 2) AS TotalSize_MB
        FROM 
            information_schema.tables
        WHERE 
            table_schema = 'python_db' 
            AND table_name = 'indianfood';
    """)
    table_info = cursor.fetchone()
    
    cursor.execute("SELECT user, COUNT(*) as recipe_count FROM indianfood GROUP BY user")
    user_data = cursor.fetchall()
    
    total_rows = sum(user['recipe_count'] for user in user_data)
    total_space_kb = float(table_info['TotalSize_KB'])
    total_space_mb = float(table_info['TotalSize_MB'])
    
    result = {
        "total_recipes": total_rows,
        "total_space_kb": total_space_kb,
        "total_space_mb": total_space_mb,
        "users": {}
    }
    
    for user in user_data:
        user_name = user['user']
        recipe_count = user['recipe_count']
        percentage = recipe_count / total_rows if total_rows else 0
        
        result['users'][user_name] = {
            "recipe_count": recipe_count,
            "space_kb": round(total_space_kb * percentage, 2),
            "space_mb": round(total_space_mb * percentage, 2),
            "percentage": round(percentage * 100, 2)
        }
    
    connection.close()
    return result

def get_system_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    os_info = f"{platform.system()} {platform.release()}"
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time
    return {
        'hostname': hostname,
        'ip_address': ip_address,
        'os_info': os_info,
        'uptime': str(uptime).split('.')[0]
    }

def get_cpu_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    per_core_usage = psutil.cpu_percent(interval=1, percpu=True)
    core_count = psutil.cpu_count(logical=False)
    logical_core_count = psutil.cpu_count(logical=True)
    try:
        cpu_temp = psutil.sensors_temperatures()['coretemp'][0].current
    except:
        cpu_temp = "N/A"
    return {
        'overall_usage': cpu_usage,
        'per_core_usage': per_core_usage,
        'physical_cores': core_count,
        'logical_cores': logical_core_count,
        'temperature': cpu_temp
    }

def get_memory_info():
    memory = psutil.virtual_memory()
    return {
        'total': round(memory.total / (1024 ** 3), 2),
        'used': round(memory.used / (1024 ** 3), 2),
        'percent': memory.percent
    }

def get_disk_info():
    disk = psutil.disk_usage('/')
    partitions = psutil.disk_partitions()
    try:
        disk_io = psutil.disk_io_counters()
        read_speed = round(disk_io.read_bytes / (1024 * 1024), 2)
        write_speed = round(disk_io.write_bytes / (1024 * 1024), 2)
    except:
        read_speed = write_speed = "N/A"
    return {
        'total': round(disk.total / (1024 ** 3), 2),
        'used': round(disk.used / (1024 ** 3), 2),
        'percent': disk.percent,
        'read_speed': read_speed,
        'write_speed': write_speed,
        'partitions': [p.mountpoint for p in partitions]
    }

def get_network_info():
    net_io = psutil.net_io_counters()
    network_interfaces = psutil.net_if_stats()
    return {
        'bytes_sent': round(net_io.bytes_sent / (1024 ** 2), 2),
        'bytes_recv': round(net_io.bytes_recv / (1024 ** 2), 2),
        'interfaces': list(network_interfaces.keys())
    }

def get_gpu_info():
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]
            return {
                'name': gpu.name,
                'temperature': gpu.temperature,
                'memory_total': round(gpu.memoryTotal / 1024, 2),
                'memory_used': round(gpu.memoryUsed / 1024, 2),
                'memory_percent': round((gpu.memoryUsed / gpu.memoryTotal) * 100, 2)
            }
        return None
    except Exception as e:
        print(f"Error getting GPU info: {e}")
        return None

@app.route('/')
def index():
    recipe_space_data = calculate_user_recipe_space()
    system_info = get_system_info()
    cpu_info = get_cpu_info()
    memory_info = get_memory_info()
    disk_info = get_disk_info()
    network_info = get_network_info()
    gpu_info = get_gpu_info()
    return render_template('index.html', 
        system_info=system_info,
        cpu_info=cpu_info,
        memory_info=memory_info,
        disk_info=disk_info,
        network_info=network_info,
        gpu_info=gpu_info,
        recipe_space_data=recipe_space_data
    )

if __name__ == '__main__':
    app.run(debug=True)
