function result = getRepresentLine2( area,trajHur ,perc)
% Algorithm 3 common sub-trajectories clustering in paper.
%   Input: area, cube-intersection information.
%          trajHur, cubes.
%          perc, p in paper.
    result = [];   
    SP = sparse(vertcat(area(:,5),area(:,6)),vertcat(area(:,6),area(:,5)),vertcat(area(:,3),area(:,1)));
    SP = full(SP);
    [r,~,v] = find(SP);
    sumSP = sum(sparse(r,v,1)>0,2);
    [m,icc] = max(sumSP);
    if perc >= 1
        minIsec = 0;
    else
        minIsec = getPerc(sumSP,perc);
    end
    
    while m >= minIsec 
        spIccOne = find(SP(icc,:) >= 1);
        a = trajHur(spIccOne',:);
        result = vertcat(result,getOne(a));
        SP(:,spIccOne) = 0;
        SP(spIccOne,:) = 0;
        [r,~,v] = find(SP);
        [m,icc] = max(sum(sparse(r,v,1)>0,2));
        if isempty(m)
            break;
        end
    end
end


function minIsec = getPerc(coreCount,perc)
    m = max(coreCount);
    countHist = hist(coreCount,0:m);
    sumCount = sum(countHist);
    countHist2 = zeros(1,m+1);
    countHist2(1) = countHist(1);
    perc2 = 1-perc;
    sumCount2 = sumCount*perc2;
    for i = 1:m
        countHist2(i+1) = countHist2(i) + countHist(i+1);
        if countHist2(i+1) >= sumCount2
            minIsec = i;
            break;
        end
    end
end


function result = getOne(trajHur)
    result = zeros(1,4);
    result(1) = mean(trajHur(:,9));
    result(6) = mean(trajHur(:,10));
    result(2) = mean(trajHur(:,3));
    result(3) = mean(trajHur(:,4));
    result(4) = avgAngle(trajHur(:,8));
    result(5) = length(trajHur(:,8));
end

function result = avgAngle(angles)
    y = sum(sind(angles)); 
    x= sum(cosd(angles));
    result = round(atan2d(y,x));
end
