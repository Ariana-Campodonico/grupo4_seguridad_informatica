
import sqlite3
from pathlib import Path

# Utiliza la misma base de datos de las aplicaciones.
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "usuarios.db"


def revisar_base_datos():
    print("=" * 55)
    print("REVISIÓN BÁSICA DE SEGURIDAD SQLITE")
    print("=" * 55)

    if not DB_PATH.exists():
        print("[AVISO] La base de datos todavía no existe.")
        print("Ejecuta primero app_segura.py para inicializarla.")
        return

    try:
        # Conexión a la base de datos local.
        with sqlite3.connect(DB_PATH) as conn:
            # Comprueba la integridad de la base de datos.
            resultado = conn.execute(
                "PRAGMA integrity_check"
            ).fetchone()[0]

            print(f"Integridad de la base de datos: {resultado}")

            # Comprueba que las tablas existentes sean conocidas.
            tablas = conn.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                AND name NOT LIKE 'sqlite_%'
            """).fetchall()

            print("\nTablas encontradas:")
            if tablas:
                for tabla in tablas:
                    print(f"- {tabla[0]}")
            else:
                print("- No se encontraron tablas de usuario.")

            # Muestra si el registro de claves foráneas está activo.
            claves_foraneas = conn.execute(
                "PRAGMA foreign_keys"
            ).fetchone()[0]

            estado = "activadas" if claves_foraneas else "desactivadas"
            print(f"\nClaves foráneas: {estado}")

            print("\nBuenas prácticas recomendadas:")
            print("- Usar consultas parametrizadas.")
            print("- No guardar contraseñas en texto plano.")
            print("- Limitar permisos de acceso al archivo .db.")
            print("- Crear copias de seguridad periódicas.")
            print("- No exponer la base de datos al directorio web.")
            print("- Mantener mensajes de error genéricos.")

    except sqlite3.Error as error:
        print(f"[ERROR] No se pudo revisar la base de datos: {error}")


if __name__ == "__main__":
    revisar_base_datos()
