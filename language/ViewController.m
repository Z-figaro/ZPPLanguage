//
//  ViewController.m
//  language
//
//  Created by figaro on 2019/4/25.
//  Copyright © 2019 figaro. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
    
    UIButton *button = [[UIButton alloc] initWithFrame:CGRectMake(200, 100, 80, 80)];
    button.titleLabel.text = NSLocalizedString(@"确定", nil);
    [self.view addSubview:button];
}


@end
