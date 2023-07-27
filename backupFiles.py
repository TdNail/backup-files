import os
import shutil
import datetime


def cleanup_old_backups(destination_dir, max_backups):
    # Coleta uma lista com os backups existentes no diretório.
    backup_folders = [f for f in os.listdir(destination_dir) if f.startswith("Backup_")]
    backup_folders.sort()

    # Verifica se excedeu o máximo de backup e exclui o primeiro que foi criado.
    if len(backup_folders) >= max_backups:
        oldest_backup = os.path.join(destination_dir, backup_folders[0])
        shutil.rmtree(oldest_backup)

def backup_files(source_dir, destination_dir, log_file, log_dir, max_backups=5):
    try:
        # Verifica se o diretório existe, se não, ele cria um novo.
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
            os.makedirs(log_dir)

        # Chama a função que verifica o quantidade de backup existentes e apagar se for necessário, neste caso o máximo é 5.
        cleanup_old_backups(destination_dir, max_backups)

        # Cria o nome do diretório de backup com data e hora
        log_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_dir_name = f"Backup_{log_time}"

        # Criar um diretório de backup único (caso já exista um diretório com o mesmo nome)
        while os.path.exists(os.path.join(destination_dir, backup_dir_name)):
            log_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_dir_name = f"Backup_{log_time}"

        # Cria o caminho completo para o diretório de backup
        backup_dir_path = os.path.join(destination_dir, backup_dir_name)
        backup_dirLog_path = os.path.join(log_dir)

        # Realiza a copia os arquivos do diretório de origem para o diretório o destino
        shutil.copytree(source_dir, backup_dir_path)

        # Cria um log com a data e hora em que o backup foi realizado e apenas edita caso seja realizado mais vezes
        log_path = os.path.join(backup_dirLog_path, f"{log_file}.txt")
        with open(log_path, "a") as log_file:
            log_file.write(f"Backup realizado em: {log_time}\n")

        print("Backup concluído com sucesso!")
    except Exception as e:
        print(f"Erro ao realizar o backup: {e}")


if __name__ == "__main__":
    source_directory = r"C:\Users\Nailson\Desktop\Backup teste python"
    destination_directory = r"C:\Users\Nailson\Desktop\Destino backup teste"
    log_directory = r"C:\Users\Nailson\Desktop\Destino backup teste\Logs"
    log_filename = "backup_log"

    backup_files(source_directory, destination_directory, log_filename, log_directory)
