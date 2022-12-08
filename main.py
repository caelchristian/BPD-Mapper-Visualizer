from final import create_app, show_plots


app = create_app()

if __name__ == '__main__':
    # GRADERS! Please uncomment this to see the plots ty
    # show_plots()
    
    app.run(debug=True)
    