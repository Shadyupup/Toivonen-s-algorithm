# coding=utf-8
import collections
import copy
import datetime
import itertools
import random
import sys


class Solution(object):
    def subsets(self, nums):
        res = []
        solution = []
        self.FindSubSet(res, nums, 0, solution)
        return res

    def FindSubSet(self, res, myInput, index, solution):
        if index == len(myInput):
            if len(solution) == 0:
                res.append([])
            else:
                res.append(solution)
            return
        solution.append(myInput[index])
        mysolution = copy.deepcopy(solution)
        self.FindSubSet(res, myInput, index + 1, mysolution)
        solution.pop()
        mysolution = copy.deepcopy(solution)
        self.FindSubSet(res, myInput, index + 1, mysolution)

    def isNagativeInfrequent(self, nagativeborder, iteration, sampleList, falseNegativeBorderSet):
        falseNegativeFlag = True
        if iteration == 1:
            return False
        counter = {}
        for item in nagativeborder[0]:
            for basket in sampleList:
                if item in basket:
                    if item not in counter.keys():
                        counter[item] = 1
                    else:
                        counter[item] += 1
                        if counter[item] >= 80:
                            falseNegativeFlag = False
                            falseNegativeBorderSet.add(item)
        for itemsTuple in nagativeborder[1:]:
            counter = {}
            for pairTuple in itemsTuple:
                for basket in sampleList:
                    flag = True
                    for item in pairTuple:
                        if item not in basket:
                            flag = False
                    if flag:
                        if pairTuple not in counter.keys():
                            counter[pairTuple] = 1
                        else:
                            counter[pairTuple] += 1
                            if counter[pairTuple] >= 80:
                                falseNegativeFlag = False
                                falseNegativeBorderSet.add(pairTuple)
        return falseNegativeFlag

    def ItemFrequent(self, frequentItemSet, lineList, res):
        counter = {}
        oneFrequent = set()
        pairFrequent = set()
        for item in frequentItemSet[0]:
            for basket in lineList:
                if item in basket:
                    if item not in counter.keys():
                        counter[item] = 1
                    else:
                        counter[item] += 1
                        if counter[item] >= 80:
                            oneFrequent.add(item)
        for itemsTuple in frequentItemSet[1:]:
            for pairTuple in itemsTuple:
                for basket in lineList:
                    flag = True
                    for item in pairTuple:
                        if item not in basket:
                            flag = False
                    if flag:
                        if pairTuple not in counter.keys():
                            counter[pairTuple] = 1
                        else:
                            counter[pairTuple] += 1
                            if counter[pairTuple] >= 80:
                                pairFrequent.add(pairTuple)
        res.append(sorted(list(oneFrequent)))
        res.append(sorted(list(pairFrequent)))


if __name__ == "__main__":
    starttime = datetime.datetime.now()
    f = open(sys.argv[1])
    lines = f.readlines()

    frequentItemSet = []
    nagativeborder = []
    count = 1
    lineList = []
    iteration = 1
    falseNegativeBorderSet = set()
    for basket in lines:
        items = basket[1:len(basket) - 2].split(",")
        basketList = []
        for num in items:
            item = int(num.strip())
            basketList.append(item)
        tmplist = copy.deepcopy(basketList)
        lineList.append(tmplist)

    # and (not Solution().isItemFrequent(frequentItemSet, iteration, lineList))
    while not Solution().isNagativeInfrequent(nagativeborder, iteration, lineList, falseNegativeBorderSet):
        print("False Negatives: " + str(sorted(list(falseNegativeBorderSet))))
        falseNegativeBorderSet = set()
        frequentItemSet = []
        nagativeborder = []
        random.seed(iteration)
        begin = random.randint(0, len(lines) - 30)
        end = begin + 30
        # sample = lines[286:316]
        sample = lines[begin:end]
        res = []

        # 原始都是string，不好处理，这里搞成int的list
        sampleList = []
        sampleSet = set()
        # 计数用
        dic = {}
        # 每个K记录频繁项
        frequent_table = set()
        infrequent_table = set()
        for basket in sample:
            items = basket[1:len(basket) - 2].split(",")
            # 用来放每个basket转成Int后的值
            basketList = set()
            for item in items:
                item = int(item.strip())
                basketList.add(item)
                sampleSet.add(item)
                if item not in dic:
                    dic[item] = 1
                else:
                    dic[item] += 1
                    if dic[item] >= 8:
                        frequent_table.add(item)
            tmp = copy.deepcopy(sorted(list(basketList)))
            sampleList.append(tmp)
        frequent_list = sorted(list(frequent_table))
        infrequent_table = sampleSet - frequent_table
        frequentItemSet.append(frequent_list)
        nagativeborder.append(sorted(list(infrequent_table)))

        count = 2
        while len(frequent_list) != 0:
            pairs_candidate = []
            pairs_candidate_set = set()
            tmp_pairs_candidate = itertools.combinations(frequent_list, count)
            # pairs_candidate = itertools.combinations(frequent_list, count)
            for tmp_pair in tmp_pairs_candidate:
                flag = True
                subset = Solution().subsets(tmp_pair)
                for tmpSet in subset:
                    if count - 2 < len(tmpSet) < count:
                        checkFrequentList = list(frequent_table)
                        if len(tmpSet) == 1:
                            if tmpSet[0] not in checkFrequentList:
                                flag = False
                        else:
                            if tuple(tmpSet) not in checkFrequentList:
                                flag = False
                if (flag):
                    pairs_candidate.append(tmp_pair)
            pairs_candidate_set = set(pairs_candidate)

            frequent_table = set()
            frequent_list = []
            dic = {}
            for pair in pairs_candidate:
                for basket in sampleList:
                    flag = True
                    for item in pair:
                        if item not in basket:
                            flag = False
                    if flag:
                        if pair not in dic:
                            dic[pair] = 1
                        else:
                            dic[pair] += 1
                            if dic[pair] >= 8:
                                frequent_table.add(pair)
                                for num in pair:
                                    frequent_list.append(num)
            if len(frequent_table) != 0:
                frequentItemSet.append(list(frequent_table))
                frequent_list = list(set(frequent_list))
                nagativeborder.append(sorted(list(pairs_candidate_set - frequent_table)))
                count += 1

        if iteration != 15:
            f = open('output/OutputForIteration_' + str(iteration) + '.txt', 'w')  # 若是'wb'就表示写二进制文件
            f.write('Sample Created:\n')
            f.write(str(sampleList) + "\n")
            f.write("frequent itemsets:\n")
            for line in frequentItemSet:
                f.write(str(line) + "\n")
            f.write("negative border:\n")
            for line in nagativeborder:
                f.write(str(line) + "\n")
            f.close()
            iteration += 1
        else:
            f = open('output/OutputForIteration_' + str(iteration) + '.txt', 'w')  # 若是'wb'就表示写二进制文件
            f.write('Sample Created:\n')
            f.write(str(sampleList) + "\n")
            f.write("frequent itemsets:\n")
            res = []
            Solution().ItemFrequent(frequentItemSet, lineList, res)
            for line in res:
                f.write(str(line) + "\n")
            # f.write(str(res) + "\n")
            f.write("negative border:\n")
            for line in nagativeborder:
                if len(line)==0:
                    break
                f.write(str(line) + "\n")
            f.close()
            iteration += 1
    endtime = datetime.datetime.now()
    print ("-----" + str(iteration - 1) + " times iteration" + "-----")
    print ("-----" + str((endtime - starttime).seconds) + " s" + "-----")
