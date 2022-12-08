from final import create_app, show_plots


app = create_app()

if __name__ == '__main__':
    show_plots()
    app.run(debug=True)
    