from appFuncs import app

if __name__=='__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    #app.run(debug=True)
    # manager = DatabaseManager.DatabaseManager()
    # columns = ['id', 'helio_id', 'battery', 'motor1', 'motor2', 'date']
    # data_types = ['int', 'varchar(127)', 'real', 'real', 'real', 'timestamp']
    # manager.createTable('appdata', 'helio_1', columns, data_types, host='cloud')
