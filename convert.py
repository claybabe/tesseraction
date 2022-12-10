import torch.onnx 

if __name__ == "__main__": 

    from tkinter import filedialog
    rules_model_path = filedialog.askopenfilename()
    model = torch.load(rules_model_path, map_location='cpu')

    
    # Conversion to ONNX 
    model.eval() 

    # Let's create a dummy input tensor  
    dummy_input = torch.ones(1, 177)  
    
    print(model(dummy_input));

    # Export the model   
    torch.onnx.export(model, dummy_input, "tesseraction.onnx")
    
    print(" ") 
    print('Model has been converted to ONNX')