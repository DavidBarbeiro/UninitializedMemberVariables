#import "XYZPerson.h"
 
@implementation XYZPerson

- (void) method1init{
	p1=nil
}

- (int )setupasd 
{
	
    p2 = nil;
    
}

- (int& )method3init 
{
	
    p3 = nil;
    
}

- (int** )method4init 
{
	
    p4 = nil;
    
}

+ (instancetype)method5init { return [[self alloc] init]; }

- (instancetype)init6
{
    if ( (self = [super init]) ) {
        self.backingStore = [NSMutableDictionary dictionary];
        self.queue = dispatch_queue_create(NULL, DISPATCH_QUEUE_CONCURRENT);
    }
    return self;
}

- (int** )method7init:(int* type1) arg1 {
	
    p7 = nil;
    
}

@end