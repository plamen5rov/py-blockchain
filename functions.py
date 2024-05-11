def unlimited_arguments(*args):
    print(args)
    for arg in args:
        print(arg)
        
        
unlimited_arguments(1,2,3,4,5)
unlimited_arguments(*[1,2,3,4,5])
    