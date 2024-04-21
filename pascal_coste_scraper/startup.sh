replace_config() {
    sed -i "s|{{DB_HOST}}|${DB_HOST}|g" config.ini
    sed -i "s|{{DB_USER}}|${DB_USER}|g" config.ini
    sed -i "s|{{DB_PASSWORD}}|${DB_PASSWORD}|g" config.ini
    sed -i "s|{{DB_DATABASE}}|${DB_DATABASE}|g" config.ini
    sed -i "s|{{DB_PORT}}|${DB_PORT}|g" config.ini

    echo "After replacement:"
    cat config.ini

}

# Check if environment variables are set
if [[ -z "$DB_HOST" || -z "$DB_USER" || -z "$DB_PASSWORD" || -z "$DB_DATABASE" || -z "$DB_PORT" ]]; then
        echo "Error: One or more required environment variables are not set."
        exit 1
fi

replace_config

python3 main.py
python3 database.py