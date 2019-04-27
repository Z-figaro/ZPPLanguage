//
//  zzzViewController.m
//  language
//
//  Created by figaro on 2019/4/25.
//  Copyright © 2019 figaro. All rights reserved.
//

#import "zzzViewController.h"

@interface zzzViewController ()

@end

@implementation zzzViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    UIButton *button = [[UIButton alloc] initWithFrame:CGRectMake(200, 100, 80, 80)];
    button.titleLabel.text = NSLocalizedString(@"取消", nil);
    
    UIButton *button1 = [[UIButton alloc] initWithFrame:CGRectMake(200, 100, 80, 80)];
    button.titleLabel.text = NSLocalizedString(@"可能性测试", nil);
    [self.view addSubview:button];
}

/*
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}
*/

@end
